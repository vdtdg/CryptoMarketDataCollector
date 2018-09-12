# CryptoMarketDataCollector (CMDC)
The goal of this project is to merge [WhiteRaBot17 Data Collector](https://github.com/WhiteRaBot17/BittrexDataCollector) and [ivopetiz crypto-database](https://github.com/ivopetiz/crypto-database).  

This application will provide you a back-end for any project that would need cryptocurrencies market data.
You will be able to store continuously live market data from any exchange in InfluxDB.   
Some exchanges don't provide full historical data, but this application can mock by using other exchange's data (if you want to backtest a trading strategy for example).


This application will collect sort, and organize financial data from a list of Crypto currencies, using [https://github.com/ccxt/ccxt](CCXT). You can set the market that you want to analyze, the coins in that market, and the time intervals you want to collect data from. 

This application requires Python 3+


#Instructions:

Configure the app  

Install dependencies :   
```pip install -r requirements.txt```

Install the database  

Configure the database  

Launch the app