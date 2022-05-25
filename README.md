
# Binance Triangular Arbitrage
Binance Triangular Arbitrage will check for each triangular arbitrage combination based on a given currency and execute three consecutive trades that result in the specified profit margin.

In the configuration file `config.yml` you can define several parameters such as the cryptocurrency you want to trade, your initial investment, the minimum profit for each trade, or enable/disable the test mode. 

### Requirement
* Python 3 (Tested with Python 3.9).
* Internet connection (Fast one if possible),

### Installation
Clone this repository and run:
```shell
pip install -r requirements.txt
```

### Configuration
Edit the file `config.yml` and add your Binance API keys.
```yaml
binance_api:
  apiKey: "<API_KEY>" #Insert your API_KEY.
  secretKey: "<secret_KEY>" #Insert your secret_KEY.
```
Then define .
```yaml
settings:
  isTest: False #Want test mode?
  base_currency: "USDT" #Currency you want to trade.
  INVESTMENT_AMOUNT_DOLLARS: 1000 #Your initial investement
  MIN_PROFIT_DOLLARS: 5 #Minimum profit per trade.
  ...
```


#### Usage
```
python3 bta.py
```
That's all, now let's make some money!

![Binance Triangular Arbitrage trading bot](https://i.ibb.co/bmfX4TV/Binnance-Triangular-Arbitrage.jpg)