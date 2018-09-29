""" This application was developed for gathering financial data
from any exchanges using ccxt with the purpose of storing it on
a local InfluxDB instance. """

__title__ = 'Crypto Market Data Collector'
__license__ = 'MIT'

import sys
import time

import ccxt
from influxdb import *

from config import *


def init_engine():
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

    return engine


def init_market_array():
    # Creating an initialization array. It will tell us if we already gathered the past data for a market.
    init_market = dict()
    for ticker in tickers:
        init_market[ticker] = False

    return init_market


def parse_timeframe(timeframe):
    amount = int(timeframe[0:-1])
    unit = timeframe[-1]
    if 'y' in unit:
        scale = 60 * 60 * 24 * 365
    elif 'M' in unit:
        scale = 60 * 60 * 24 * 30
    elif 'w' in unit:
        scale = 60 * 60 * 24 * 7
    elif 'd' in unit:
        scale = 60 * 60 * 24
    elif 'h' in unit:
        scale = 60 * 60
    else:
        scale = 60  # 1m by default
    return amount * scale


def parse_ticker(ticker):
    ret = ticker.split(".")
    err = ""
    if len(ret) != 3:
        err = "Wrong ticker : {}".format(ticker)
    return ret[0], ret[1], ret[2], err


def init_ticker_dict(tickers):
    td = {}
    for t in tickers:
        e, m, du, err = parse_ticker(t)
        if err != "":
            return td
        td[t] = {'date_last': 0,
                 'duration': parse_timeframe(du)
                 }

    return td


def get_data(ticker, ticker_dict, init_dict, engine):
    exchange, market, duration, err = parse_ticker(ticker)
    if err != "":
        print("Error parsing ticker : {}".format(err))
        return

    # Init the exchange
    ex_c = getattr(ccxt, exchange)
    ex = ex_c({
        # 'apiKey': '',
        # 'secret': '',
        'timeout': 30000,
        'enableRateLimit': True
    })
    ex.load_markets()

    # We need to check if the exchange is able to return OHLCV data before doing anything.
    if not ex.has['fetchOHLCV']:
        print("Impossible to get OHLCV data from this exchange : {}".format(exchange))
        return

    ex_has_ticker = False
    for t in ex.symbols:
        if t == market:
            ex_has_ticker = True
            break

    if not ex_has_ticker:
        print("Can't get data from this ticker : {}".format(ticker))
        return

    # Getting either 100 timeframe history or last candle (or approx.)
    mult = 2
    if not init_dict[ticker]:
        mult = 100
        init_dict[ticker] = True
    last_date = (ex.milliseconds() - mult * ex.parse_timeframe(duration) * 1000)
    data = ex.fetchOHLCV(market, duration, since=last_date)
    print("Retrieved {} {} {} data : {}".format(exchange, market, duration, data))

    store_data(data, duration, engine, exchange, market)
    return


def get_historical_data(engine, ticker, limit=""):
    if limit == "":
        limit = 1000000000000000
    else:
        limit = int(limit)
    exchange, market, duration, err = parse_ticker(ticker)
    if err != "":
        print("Error parsing ticker : {}".format(err))
        return

    # Init the exchange
    ex_c = getattr(ccxt, exchange)
    ex = ex_c({
        # 'apiKey': '',
        # 'secret': '',
        'timeout': 30000,
        'enableRateLimit': True
    })
    ex.load_markets()

    # We need to check if the exchange is able to return OHLCV data before doing anything.
    if not ex.has['fetchOHLCV']:
        return

    ex_has_ticker = False
    for t in ex.symbols:
        if t == market:
            ex_has_ticker = True
            break

    if not ex_has_ticker:
        print("Can't get historical data from this ticker : {}".format(ticker))
        return

    print("Getting historical data of {}, be patient...".format(ticker))

    mult = 200  # TODO : optimize this value according to the exchange.
    if exchange == 'poloniex':
        mult = 1000
    start = ex.milliseconds() - mult * ex.parse_timeframe(duration) * 1000  # x1000 again to get millisec
    count = 0
    while count*mult < limit:
        count += 1
        # Get 1000 candles, then recalculate the since and start or whatever
        data = ex.fetchOHLCV(market, duration, since=start, limit=mult+1)
        print("... Fetched {} candles.".format(count * mult))
        if not data or len(data) == 1:
            print("Got full history of {}".format(ticker))
            return
        start = start - mult * ex.parse_timeframe(duration) * 1000
        store_data(data, duration, engine, exchange, market)
        time.sleep(1.1 * ex.rateLimit / 1000)

    print("Got {}/{} candles of {}".format(count*mult, limit, ticker))


def store_data(data, duration, engine, exchange_name, market):
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
                "open": candle[1] + 0.0,
                "high": candle[2] + 0.0,
                "low": candle[3] + 0.0,
                "close": candle[4] + 0.0,
                "volume": candle[5] + 0.0
            }
        })

    # Then data is added into influxdb.
    engine.write_points(json_body, time_precision='ms')


if __name__ == "__main__":
    # Reading and parsing options.
    sys.argv.append("")
    if sys.argv[1] == "get_history":
        # In this case we just init the engine and start the process of carefully getting history data.
        sys.argv.append("")
        engine = init_engine()
        get_historical_data(engine, sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "run":
        # In this case, we read and transform the list of tickers into a dict that will remember the last time
        # the data was get. By doing so we reduce the number of API calls.
        engine = init_engine()
        ticker_dict = init_ticker_dict(tickers)
        init_dict = init_market_array()
        while True:
            for ticker in ticker_dict:
                dl = ticker_dict[ticker]["date_last"]
                d = ticker_dict[ticker]["duration"]
                if time.time().__int__() > dl + (d/2).__int__():
                    get_data(ticker, ticker_dict, init_dict, engine)
                    ticker_dict[ticker]["date_last"] = time.time().__int__()
                else:
                    print("Nothing to do, sleeping...")
                    time.sleep(5)

    else:
        print("Usage : python3 <path_to_src>/app.py [command] [value] [number]\n\n"
              + "Command list: \n"
              + "  run : collect live data from the tickers specified in config.py\n"
              + "  get_history : get the historical data from the ticker defined in value. You can set a maximum"
                "number of period you want to download. See the config file for the syntax of the ticker.\n\n"
              + "Examples :\n"
              + "  python3 app.py get_history gdax.BTC/USD.1h\n"
              + "  python3 app.py get_history gdax.BTC/USD.1h 1500\n"
              + "  python3 app.py run\n")
