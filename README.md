# CryptoMarketDataCollector (CMDC)
The goal of this project is to merge [WhiteRaBot17 Data Collector](https://github.com/WhiteRaBot17/BittrexDataCollector) and [ivopetiz crypto-database](https://github.com/ivopetiz/crypto-database).  

This application will provide you a back-end for any project that would need cryptocurrencies market data.
You will be able to store continuously live market data from any exchange in InfluxDB.   
Some exchanges don't provide full historical data, but this application can mock by using other exchange's data _(feature still in development)_.  


This application will collect sort, and organize financial data from a list of Crypto currencies, using [CCXT](https://github.com/ccxt/ccxt). You can set the market that you want to analyze, the coins in that market, and the time intervals you want to collect data from. 

This application requires Python 3.5+. Also, this has only been tested on Lubuntu 18.04


# Installation

### Requirements  
Python 3.5+ required.

The package ```python3-dev``` and ```gcc``` are required : 
```bash
sudo apt-get install gcc python3-dev -y
``` 

Python packages required : ```pip install -r requirements.txt```

Not required, but advised if you want a nice visualization of your data : [Chronograf](https://portal.influxdata.com/downloads#influxdb).   

### Install the database  
This tool uses InfluxDB, we're going to set up one. If you already have one, then go to ```src/config.py``` to connect to your db.

Run these in the directory you want:   
      
```bash
wget https://dl.influxdata.com/influxdb/releases/influxdb_1.6.2_amd64.deb
sudo dpkg -i influxdb_1.6.2_amd64.deb
```

Then we can launch it:
```bash
sudo systemctl enable influxdb.service
sudo systemctl start influxdb.service
influx
```

No need to create user or db, it will be done by CMDC.

# Instructions

### Configuration
In ```src/config```, you can find everything that can be configured, see the comments on each line for more info.

### Launch the app
Simply ```python3 src/app.py run```, the config is made via ```src/config.py```.   
If you want to get historical data about an exchange, do : ```python3 src/app.py get_history <ticker>``` where 'ticker' is, for example : poloniex.BTC/USDT.1h (see config.py for more info on tickers).

### Launch it as a service
Complete fields in the ```cmdc.service``` file. You just have to put your unix username and paths to python and the source.   
Then :   
```bash
sudo cp cmdc.service /lib/systemd/system/cmdc.service
sudo systemctl start cmdc.service
```
Make sure you have configured everything you want. Nonetheless, if you need to add or remove a ticker from the config file, just do it and then :
```bash
sudo systemctl reload cmdc.service
```


# What's next ?

## v0.3 (nov. 2018)
- Optional account data collection (trade history, portfolio etc...)     
- Complete setup, launch only one command and it makes the complete installation.      
- Can be deployed as a service.  

### ***v0.3** will be the last version, there will be no more functionnality afterwards. There might be correcting fixes nevertheless.*  
