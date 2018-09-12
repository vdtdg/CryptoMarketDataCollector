''' This application was developed for gathering financial data
from the Bittrex API with the purpose of storing it locally, and to be
easily accessed by different analysis tools including Excel, and Python, or
any software that can deal with CSV files. '''


__title__ = 'Bittrex Data Collector'
__author__ = 'Jacob Weeks'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017, Jacob Weeks'

import json

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Coins(Base):
    
    __tablename__ = "Coin Data"
 
    id = Column(Integer, primary_key=True)
    open_ = Column(Float)
    high_ = Column(Float)
    low_ = Column(Float)
    close_ = Column(Float)
    volume_ = Column(Float)
    time_ = Column(String())
    BV_ = Column(Float)

    def __init__(self, open_, high_,low_,close_, volume_,time_,BV_):
        self.open_ = open_
        self.high_ = high_
        self.low_ = low_
        self.close_ = close_
        self.volume_ = volume_
        self.time_ = time_
        self.BV_ = BV_
        