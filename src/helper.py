""" This application was developed for gathering financial data
from any exchanges using ccxt with the purpose of storing it on
a local InfluxDB instance. """


from influxdb import InfluxDBClient
from influxdb import SeriesHelper

from config import *

__title__ = 'Crypto Market Data Collector'
__license__ = 'MIT'


class InsertMarketDataHelper(SeriesHelper):
    class Meta:

        series_name = '{exchange}.{market}.{duration}'

        fields = ['time', 'open', 'high', 'low', 'close', 'volume']

        timestamp = fields[0]  # get the timestamp of the candle

        tags = ['exchange', 'market', 'duration']

        client = InfluxDBClient(host=db_host, port=db_port, username=db_user, password=db_pw, database=db_name)

        bulk_size = 1
        autocommit = True

        def __init__(self, open_, high_, low_, close_, volume_, time_):
            self.open = open_
            self.high = high_
            self.low = low_
            self.close = close_
            self.volume = volume_
            self.time = time_
