# InfluxDB configuration
db_host = 'localhost'
db_port = 8086
db_user = 'CryptoMarketDataCollector'
db_pw = '01101011'
db_name = 'CryptoMarketData'

# Throw in the list the tickers you want your data from.
# Tickers have this syntax : exchange.market.duration
# Examples: "gdax.BTC/USD.1d", "bittrex.LTC/USDT.4h"
# List of supported exchange : ['_1broker', '_1btcxe', 'acx', 'allcoin', 'anxpro', 'anybits', 'bcex', 'bibox', 'bigone', 'binance', 'bit2c', 'bitbank', 'bitbay', 'bitfinex', 'bitfinex2', 'bitflyer', 'bitforex', 'bithumb', 'bitkk', 'bitlish', 'bitmarket', 'bitmex', 'bitsane', 'bitso', 'bitstamp', 'bitstamp1', 'bittrex', 'bitz', 'bl3p', 'bleutrade', 'braziliex', 'btcalpha', 'btcbox', 'btcchina', 'btcexchange', 'btcmarkets', 'btctradeim', 'btctradeua', 'btcturk', 'btcx', 'bxinth', 'ccex', 'cex', 'chbtc', 'chilebit', 'cobinhood', 'coinbase', 'coinbaseprime', 'coinbasepro', 'coincheck', 'coinegg', 'coinex', 'coinexchange', 'coinfalcon', 'coinfloor', 'coingi', 'coinmarketcap', 'coinmate', 'coinnest', 'coinone', 'coinsecure', 'coinspot', 'cointiger', 'coolcoin', 'crypton', 'cryptopia', 'deribit', 'dsx', 'ethfinex', 'exmo', 'exx', 'fcoin', 'flowbtc', 'foxbit', 'fybse', 'fybsg', 'gatecoin', 'gateio', 'gdax', 'gemini', 'getbtc', 'hadax', 'hitbtc', 'hitbtc2', 'huobi', 'huobicny', 'huobipro', 'ice3x', 'independentreserve', 'indodax', 'itbit', 'jubi', 'kraken', 'kucoin', 'kuna', 'lakebtc', 'lbank', 'liqui', 'livecoin', 'luno', 'lykke', 'mercado', 'mixcoins', 'negociecoins', 'nova', 'okcoincny', 'okcoinusd', 'okex', 'paymium', 'poloniex', 'qryptos', 'quadrigacx', 'quoinex', 'rightbtc', 'southxchange', 'surbitcoin', 'theocean', 'therock', 'tidebit', 'tidex', 'uex', 'urdubit', 'vaultoro', 'vbtc', 'virwox', 'wex', 'xbtce', 'yobit', 'yunbi', 'zaif', 'zb']
tickers = ["bittrex.BTC/USDT.1h", "bittrex.BTC/USDT.1d", "gdax.BTC/USD.1h", "poloniex.BTC/USDT.5m"]
