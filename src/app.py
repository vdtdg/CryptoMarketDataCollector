""" This application was developed for gathering financial data
from any exchanges using ccxt with the purpose of storing it on
a local InfluxDB instance. """

__title__ = 'Crypto Market Data Collector'
__license__ = 'MIT'

import ccxt
import time

from helper import *


def init():
    # Create an engine that stores data in the influx db
    engine = InfluxDBClient(host=db_host, port=db_port, username=db_user, password=db_pw, database=db_name)

    # Getting or Creating the database
    list_db = engine.get_list_database()
    db_exist = False
    for db in list_db:
        if db['name'] == db_name:
            db_exist = True
            break

    if not db_exist:
        engine.create_database(db_name)

    engine.switch_database(db_name)

    # Getting or Creating the user "CryptoMarketDataCollector" for the db
    list_users = engine.get_list_users()
    user_exist = False
    for user in list_users:
        if user['user'] == db_user:
            user_exist = True
            break

    if not user_exist:
        engine.create_user(db_user, db_pw, admin=True)

    engine.switch_user(db_user, db_pw)

    # Creating an infinity retention policy so that data is not erased from the db
    engine.create_retention_policy('no_delete_policy', 'INF', replication="1", database=db_name, default=True)

    # Creating an initialization array. It will tell us if we already gathered the past data for a market.
    init_market = dict()
    for market in markets:
        for duration in durations:
            for exchange in exchanges:
                init_market[market+'-'+duration+'-'+exchange] = False

    return engine, init_market


def get_data(exchange_name, market, durations, init_dict, engine):
    # Init the exchange
    ex_c = getattr(ccxt, exchange_name)
    ex = ex_c({
        # 'apiKey': '',
        # 'secret': '',
        'timeout': 30000,
        'enableRateLimit': True
    })
    ex.load_markets()

    # We need to check if the exchange is able to return OHLCV data, else we get the ticker data TODO
    if not ex.has['fetchOHLCV']:
        return

    # Creating a correpondance between market IDs and market SYMBOLs
    translate_id_symbol = dict()
    for symbol in ex.symbols:
        translate_id_symbol[ex.market_id(symbol)] = symbol

    # Getting either max history or last candle for each durations
    for duration in durations:
        if not init_dict[market + '-' + duration + '-' + exchange_name]:
            data = ex.fetchOHLCV(translate_id_symbol[market], duration)
            init_dict[market + '-' + duration + '-' + exchange_name] = True
        else:
            last_date = (ex.milliseconds() - ex.parse_timeframe(duration) * 1000)
            data = ex.fetchOHLCV(translate_id_symbol[market], duration, since=last_date)
            print("Retrieved {} {} {} candle : {}".format(exchange_name, market, duration, data[0]))
            time.sleep(ex.rateLimit / 1000)

        # Storing data
        json_body = []
        for candle in data:
            json_body.append({
                "measurement": exchange_name,
                "tags": {
                    "duration": duration,
                    "market": market
                },
                "time": candle[0],
                "fields": {
                    "open": candle[1],
                    "high": candle[2],
                    "low": candle[3],
                    "close": candle[4],
                    "volume": candle[5]
                }
            })

        engine.write_points(json_body, time_precision='ms')
    return


if __name__ == "__main__":
    engine, init_dict = init()

    while True:
        for market in markets:
            for exchange in exchanges:
                get_data(exchange, market, durations, init_dict, engine)
