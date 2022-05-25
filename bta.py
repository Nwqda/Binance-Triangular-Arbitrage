# -*- coding: utf-8 -*-

# Author:   Naqwada (RuptureFarm 1029) <naqwada@pm.me>
# License:  MIT License (http://www.opensource.org/licenses/mit-license.php)
# Docs:     https://github.com/Nwqda/Binance-Triangular-Arbitrage
# Website:  http://samy.link/
# Linkedin: https://www.linkedin.com/in/samy-younsi/
# Note:     FOR EDUCATIONAL PURPOSE ONLY.

from datetime import datetime
import pandas as pd
import ccxt
import yaml
import math
import time
import os

def banner():
  BinanceTriangularArbitrageLogo = """                                                    
 ______  __                                   
|   __ \|__|.-----..---.-..-----..----..-----.
|   __ <|  ||     ||  _  ||     ||  __||  -__|
|______/|__||__|__||___._||__|__||____||_____|                                              
 _______        __                              __              
|_     _|.----.|__|.---.-..-----..-----..--.--.|  |.---.-..----.
  |   |  |   _||  ||  _  ||     ||  _  ||  |  ||  ||  _  ||   _|
  |___|  |__|  |__||___._||__|__||___  ||_____||__||___._||__|  
                                 |_____|                        
 _______        __     __  __                               
|   _   |.----.|  |--.|__||  |_ .----..---.-..-----..-----. 
|       ||   _||  _  ||  ||   _||   _||  _  ||  _  ||  -__| 
|___|___||__|  |_____||__||____||__|  |___._||___  ||_____| 
                                             |_____|        
          
      \033[1;93mBinance Triangular Arbitrage\033[1;m                  
\033[1;97mAuthor:\033[1;m   \033[1;92mNaqwada (RuptureFarm 1029)\033[1;m
\033[1;97mDocs:\033[1;m     \033[1;92mhttps://github.com/Nwqda/Binance-Triangular-Arbitrage\033[1;m
\033[1;97mLicense:\033[1;m  \033[1;92mMIT License (http://www.opensource.org/licenses/mit-license.php)\033[1;m
\033[1;97mWebsite:\033[1;m  \033[1;92mhttp://samy.link/\033[1;m      
  """
  return print("\033[1;94m{}\033[1;m".format(BinanceTriangularArbitrageLogo))

def load_config_vars(filename):
  config_file = os.path.isfile(filename) 
  if not config_file:
    print("\033[1;93mThe configuration file \"{}\" cannot be found.\033[1;m For more information please consult the documentation on GitHub (https://github.com/Nwqda/Binance-Triangular-Arbitrage).".format(filename))

  with open("config.yml", "r") as file:
    data = yaml.load(file, Loader=yaml.loader.SafeLoader)
    return data

# Get all possible triangular arbitrage combinations from Binance.
def get_crypto_combinations(market_symbols, base):
    combinations = []
    for sym1 in market_symbols:   
        sym1_token1 = sym1.split("/")[0]
        sym1_token2 = sym1.split("/")[1]   
        if (sym1_token2 == base):
            for sym2 in market_symbols:
                sym2_token1 = sym2.split("/")[0]
                sym2_token2 = sym2.split("/")[1]
                if (sym1_token1 == sym2_token2):
                    for sym3 in market_symbols:
                        sym3_token1 = sym3.split("/")[0]
                        sym3_token2 = sym3.split("/")[1]
                        if((sym2_token1 == sym3_token1) and (sym3_token2 == sym1_token2)):
                            combination = {
                                "base":sym1_token2,
                                "intermediate":sym1_token1,
                                "ticker":sym2_token1,
                            }
                            combinations.append(combination)
    return combinations
        

def fetch_current_ticker_price(ticker):
    ticker_details = exchange.fetch_ticker(ticker)
    close_price = ticker_details["close"] if ticker_details is not None else None
    market = exchange.load_markets()
    orderbook = exchange.fetch_order_book(ticker)
    bids = orderbook["bids"]
    asks = orderbook["asks"]

    if not bids or not asks:
        return 0

    ticker_price = (bids[0][0] + asks[0][0])/2
    return ticker_price

def check_buy_buy_sell(scrip1, scrip2, scrip3,initial_investment):
    investment_amount1 = initial_investment
    current_price1 = fetch_current_ticker_price(scrip1)
    final_price = 0
    scrip_prices = {}
    
    if current_price1 != 0:
        buy_quantity1 = round(investment_amount1 / current_price1, 8)*skim
        time.sleep(1)

        investment_amount2 = buy_quantity1     
        current_price2 = fetch_current_ticker_price(scrip2)
        if current_price2 != 0:
            buy_quantity2 = round(investment_amount2 / current_price2, 8)*skim
            time.sleep(1)

            investment_amount3 = buy_quantity2     
            current_price3 = fetch_current_ticker_price(scrip3)
            if current_price3 != 0:
                sell_quantity3 = buy_quantity2
                final_price = round(sell_quantity3 * current_price3,3)
                scrip_prices = {scrip1 : current_price1, scrip2 : current_price2, scrip3 : current_price3}

    if(verbose):
        print("BUY BUY SELL: {} -> {} -> {}   Return: {}".format(scrip1, scrip2, scrip3, final_price))
                
    return final_price, scrip_prices

def check_buy_sell_sell(scrip1, scrip2, scrip3,initial_investment):
    investment_amount1 = initial_investment
    current_price1 = fetch_current_ticker_price(scrip1)
    final_price = 0
    scrip_prices = {}
    if current_price1 != 0:
        buy_quantity1 = round(investment_amount1 / current_price1, 8)*skim
        time.sleep(1)

        investment_amount2 = buy_quantity1     
        current_price2 = fetch_current_ticker_price(scrip2)
        
        if current_price2 != 0:
            sell_quantity2 = buy_quantity1
            sell_price2 = round(sell_quantity2 * current_price2,8)
            time.sleep(1)

            investment_amount3 = sell_price2     
            current_price3 = fetch_current_ticker_price(scrip3)
            if current_price3 != 0:
                sell_quantity3 = sell_price2
                final_price = round(sell_quantity3 * current_price3,3)
                scrip_prices = {scrip1 : current_price1, scrip2 : current_price2, scrip3 : current_price3}
    if(verbose):
        print("BUY BUY SELL: {} -> {} -> {}   Return: {}".format(scrip1, scrip2, scrip3, final_price))

    return final_price,scrip_prices

def check_profit_loss(total_price_after_sell, initial_investment, transaction_brokerage, min_profit):
    apprx_brokerage = (transaction_brokerage * initial_investment/100 * 3)
    min_profitable_price = initial_investment + apprx_brokerage + min_profit
    profit_loss = round(total_price_after_sell - min_profitable_price,3)
    return profit_loss

def place_buy_order(scrip, quantity, limit, balance):
    print("BUYING: {} {} at {}".format(quantity, scrip, fetch_current_ticker_price(scrip)))
    if not isTest:
        quantity = quantity*skim
        order = exchange.create_limit_buy_order(scrip, quantity, limit)
    else:
        params = {
            "test": True
        }
        order = exchange.create_order(scrip, "limit", "buy", quantity, limit, params)
    time.sleep(1)
    return order

def place_sell_order(scrip, quantity, limit):
    print("SELLING: {} {} at {}".format(quantity, scrip, fetch_current_ticker_price(scrip)))
    if not isTest:
        order = exchange.create_limit_sell_order(scrip, quantity, limit)
    else:
        params = {
            "test": True
        }
        order = exchange.create_order(scrip, "limit", "buy", quantity, limit, params)

    time.sleep(1)
    return order 

def place_trade_orders(type, scrip1, scrip2, scrip3, initial_amount, scrip_prices):
    final_amount = 0.0

    if type == "BUY_BUY_SELL":

        inter = scrip1.split("/")[0]
        s1_price = scrip_prices[scrip1]
        s1_quantity = initial_amount/s1_price
        bal = exchange.fetch_balance()
        inter_init_amount = bal[inter]["free"]
        order1 = place_buy_order(scrip1, s1_quantity, s1_price, initial_amount)

        start = time.time()
        if not isTest:
            while(1):
                if time.time() - start >= 20:
                    print("Cancelling order and retrying...")
                    exchange.cancel_order(order1["id"], scrip1, {"type": "BUY"})
                    s1_price = fetch_current_ticker_price(scrip1)
                    s1_quantity = initial_amount/s1_price
                    order1 = place_buy_order(scrip1, s1_quantity, s1_price, initial_amount)
                    start = time.time()

                print("Waiting for {}".format(inter))
                time.sleep(2)
                BALANCE = exchange.fetch_balance() #update balances
                quantity = BALANCE[inter]
                s1_quantity = quantity["free"]
                if s1_quantity > inter_init_amount:
                    break

        print("You now have ".format(s1_quantity, inter))
        tick = scrip2.split("/")[0]
        s2_price = scrip_prices[scrip2]
        adj_price = math.ceil(s2_price * 100000000)/100000000
        s2_quantity = s1_quantity/adj_price
        bal = exchange.fetch_balance()
        tick_init_amount = bal[tick]["free"]
        order2 = place_buy_order(scrip2, s2_quantity, s2_price, s1_quantity)

        start = time.time()
        if not isTest:
            while(1):

                if time.time() - start >= 20:
                    print("Cancelling order and retrying...")
                    exchange.cancel_order(order2["id"], scrip2, {"type": "BUY"})
                    s2_price = fetch_current_ticker_price(scrip2)
                    adj_price = math.ceil(s2_price * 100000000)/100000000
                    s2_quantity = s1_quantity/adj_price
                    order2 = place_buy_order(scrip2, s2_quantity, s2_price, s1_quantity)
                    start = time.time()

                print("Waiting for {}".format(tick))
                time.sleep(2)
                BALANCE = exchange.fetch_balance()
                quantity2 = BALANCE[tick]
                s2_quantity = quantity2["free"]
                if s2_quantity > tick_init_amount:
                    break

        print("You now have {} {}".format(s2_quantity, tick))
        base = scrip3.split("/")[1]
        s3_price = scrip_prices[scrip3]
        s3_quantity = s2_quantity
        bal = exchange.fetch_balance()
        base_init_amount = bal[base]["free"]
        order3 = place_sell_order(scrip3, s3_quantity, s3_price)

        start = time.time()
        if not isTest:
            while(1):

                if time.time() - start >= 20:
                    print(f"Cancelling order and retrying...")
                    exchange.cancel_order(order3["id"], scrip3, {"type": "SELL"})
                    s3_price = fetch_current_ticker_price(scrip3)
                    s3_quantity = s2_quantity
                    order3 = place_sell_order(scrip3, s3_quantity, s3_price)
                    start = time.time()

                print("Waiting for {}".format(base))
                time.sleep(2)
                BALANCE = exchange.fetch_balance()
                quantity3 = BALANCE[base]
                s3_quantity = quantity3["free"]
                if s3_quantity > base_init_amount:
                    break

        print("You now have {} {}".format(s3_quantity, base))

    elif type == "BUY_SELL_SELL":
        inter = scrip1.split("/")[0]
        s1_price = scrip_prices[scrip1]
        s1_quantity = initial_amount/s1_price
        bal = exchange.fetch_balance()
        inter_init_amount = bal[inter]["free"]
        order1 = place_buy_order(scrip1, s1_quantity, s1_price, initial_amount)

        start = time.time()
        if not isTest:
            while(1): 
                if time.time() - start >= 20:
                    print("Cancelling order and retrying...")
                    exchange.cancel_order(order1["id"], scrip1, {"type": "BUY"})
                    s1_price = fetch_current_ticker_price(scrip1)
                    s1_quantity = initial_amount/s1_price
                    order1 = place_buy_order(scrip1, s1_quantity, s1_price, initial_amount)
                    start = time.time()

                print("Waiting for {}".format(inter))
                time.sleep(2)
                BALANCE = exchange.fetch_balance() #update balances
                quantity = BALANCE[inter]
                s1_quantity = quantity["free"]
                if s1_quantity > inter_init_amount:
                    break         

        print("You now have {} {}".format(s1_quantity, inter))
        tick = scrip2.split("/")[1]
        s2_price = scrip_prices[scrip2]
        s2_quantity = s1_quantity
        bal = exchange.fetch_balance()
        tick_init_amount = bal[tick]["free"]
        order2 = place_sell_order(scrip2, s2_quantity, s2_price)

        start = time.time()
        if not isTest:
            while(1):
                if time.time() - start >= 20:
                    print("Cancelling order and retrying...")
                    exchange.cancel_order(order2["id"], scrip2, {"type": "SELL"})
                    s2_price = fetch_current_ticker_price(scrip2)
                    s2_quantity = s1_quantity
                    order2 = place_sell_order(scrip2, s2_quantity, s2_price)
                    start = time.time()

                print(f"Waiting for {tick}")
                time.sleep(2)
                BALANCE = exchange.fetch_balance()
                quantity2 = BALANCE[tick]
                s2_quantity = quantity2["free"]
                if s2_quantity > tick_init_amount:
                    break

        print("You now have {} {}".format(s2_quantity, tick))
        base = scrip3.split("/")[1]
        s3_price = scrip_prices[scrip3]
        s3_quantity = s2_quantity
        bal = exchange.fetch_balance()
        base_init_amount = bal[base]["free"]
        order3  = place_sell_order(scrip3, s3_quantity, s3_price)

        start = time.time()
        if not isTest:
            while(1):
                if time.time() - start >= 20:
                    print("Cancelling order and retrying...")
                    exchange.cancel_order(order3["id"], scrip3, {"type": "SELL"})
                    s3_price = fetch_current_ticker_price(scrip3)
                    s3_quantity = s2_quantity*s2_price
                    order3 = place_sell_order(scrip3, s3_quantity, s3_price)
                    start = time.time()

                print("Waiting for {}".format(base))
                time.sleep(2)
                BALANCE = exchange.fetch_balance()
                quantity3 = BALANCE[base]
                s3_quantity = quantity3["free"]
                if s3_quantity > base_init_amount:
                    break
        print("You now have {} {}".format(s3_quantity, base))    
    return final_amount

def perform_triangular_arbitrage(scrip1, scrip2, scrip3, arbitrage_type, initial_investment, 
                               transaction_brokerage, min_profit):
    final_price = 0.0
    if(arbitrage_type == "BUY_BUY_SELL"):
        final_price, scrip_prices = check_buy_buy_sell(scrip1, scrip2, scrip3,initial_investment)
        
    elif(arbitrage_type == "BUY_SELL_SELL"):
        final_price, scrip_prices = check_buy_sell_sell(scrip1, scrip2, scrip3,initial_investment)
        
    profit_loss = check_profit_loss(final_price,initial_investment, transaction_brokerage, min_profit)

    if profit_loss > 0:
        print("PROFIT-{}:{}, {}, {}, {}, Profit/Loss: {}".format(datetime.now().strftime('%H:%M:%S'), arbitrage_type, scrip1, scrip2, scrip3, round(final_price-initial_investment,3), ))
        place_trade_orders(arbitrage_type, scrip1, scrip2, scrip3, initial_investment, scrip_prices)

def truncate(number, digits) -> float:
    nbDecimals = len(str(number).split(".")[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


banner()
filename = "config.yml"
config = load_config_vars(filename)

verbose = config["settings"]["verbose"]
INVESTMENT_AMOUNT_DOLLARS = config["settings"]["INVESTMENT_AMOUNT_DOLLARS"]
MIN_PROFIT_DOLLARS = config["settings"]["MIN_PROFIT_DOLLARS"]
BROKERAGE_PER_TRANSACTION_PERCENT = config["settings"]["BROKERAGE_PER_TRANSACTION_PERCENT"]
skim = config["settings"]["skim"]
base_currency = config["settings"]["base_currency"]
isTest = config["settings"]["isTest"]

exchange = ccxt.binance({
    "apiKey": config["binance_api"]["apiKey"],
    "secret": config["binance_api"]["secretKey"],
    "options": { "adjustForTimeDifference": True }
})


markets = exchange.fetchMarkets()
market_symbols = [market["symbol"] for market in markets]
print("Total of market symbols: {}".format(len(market_symbols)))

combinations = get_crypto_combinations(market_symbols, base_currency)
print("Total of crypto combinations: {}".format(len(combinations)))

cominations_df = pd.DataFrame(combinations)
cominations_df.head()

BALANCE = exchange.fetch_balance()
BASE_CURRENCY_BALANCE = BALANCE[base_currency]

print("Initial investment: {}\n".format(INVESTMENT_AMOUNT_DOLLARS))

while(1):
    for combination in combinations:
            base = combination["base"]
            intermediate = combination["intermediate"]
            ticker = combination["ticker"]

            s1 = f"{intermediate}/{base}"    # Eg: BTC/ADA
            s2 = f"{ticker}/{intermediate}"  # Eg: ETH/BTC
            s3 = f"{ticker}/{base}"          # Eg: ETH/ADA

            # Check triangular arbitrage for buy-buy-sell 
            perform_triangular_arbitrage(s1, s2, s3, "BUY_BUY_SELL", INVESTMENT_AMOUNT_DOLLARS, BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
            time.sleep(1) 

            # Check triangular arbitrage for buy-sell-sell 
            perform_triangular_arbitrage(s3, s2, s1, "BUY_SELL_SELL", INVESTMENT_AMOUNT_DOLLARS, BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
            time.sleep(1) 

    print("The script has executed all combinations. Restart from the beginning...")