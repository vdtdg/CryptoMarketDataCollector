''' This application was developed for gathering financial data
from the Bittrex API with the purpose of storing it locally, and to be
easily accessed by different analysis tools including Excel, and Python, or
any software that can deal with CSV files. (exported from .db files) '''


__title__ = 'Bittrex Data Collector'
__author__ = 'Jacob Weeks'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017, Jacob Weeks'


import requests
import os
import datetime
import time 

from models.data import *

#Set this to the market you want to analyze
MARKET = "BTC"

#Set the coins you want to analyze
COIN_LIST = ['ETH', 'NEO']

#Set the list of intervals
INTERVAL_LIST = ['oneMin','fiveMin','thirtyMin','Hour']


def store_data(session, data):
    for interval in data['result']:
        open_ = interval['O'] 
        high_ = interval['H']
        low_ =  interval['L']
        close_ = interval['C']
        volume_ = interval['V']
        time_ = interval['T']
        BV_ = interval['BV']
        newDataRow = Coins(open_,high_,low_,close_,volume_,time_,BV_)
        session.add(newDataRow)
        session.commit()
    return


def main(market,coin, interval):
    date_today = str(datetime.date.today())
    new_sub_dir = coin + "-" + date_today + "-" + interval
    try:
        os.mkdir(new_sub_dir)
    except Exception:
        return

    # Create an engine that stores data in the local sub directory

    engine = create_engine('sqlite:///'+new_sub_dir+'/'+coin+'-'+interval+'.db')

    # Create all tables in the engine.
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    
    ## SQLAlchemy DBsession ##
    session = DBSession()

    # Request the financial data from the API
    try:
        s = requests.Session()
        api_url = 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName='+market+'-'\
                                            + coin + '&tickInterval='+ interval
        time.sleep(2)
        page = s.get(api_url)
        page_response = page.text
        data = json.loads(page_response)
    except Exception:
        return


    #Store the Data into the new database
    store_data(session, data)

    return

if __name__ == "__main__":
    for interval in INTERVAL_LIST:
        for coin in COIN_LIST:
            main(MARKET,coin,interval)


