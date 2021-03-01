import requests
import time
import os
import alpaca_trade_api as tradeapi
from iexfinance.stocks import Stock
import logging
import datetime as dt
from datetime import datetime


global dir_path
dir_path = os.path.dirname(__file__)

## Read in credentials from credentials file
global alpacaKey
global alpacaSecretKey
global iexkey



try:
    with open(dir_path+'/credentials', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split('=')
            if line[0] == 'iexkey':
                iexkey = line[1].strip()
            if line[0]=='alpacakey':
                alpacaKey = line[1].strip()
            if line[0]=='alpacasecretkey':
                alpacaSecretKey = line[1].strip()
except Exception as e:
    raise Exception('No "credentials" file.')

## Read in ticker from txt file
global ticker
global move_trigger
global trade_period
global hour_offset
base = "https://oil-trader-api.herokuapp.com"

try:
    base = base + '/parameters'
    response = requests.get(base)
    print(response)
    response = response.text
    print(response)
    
    ticker = response['ticker']
    move_trigger = response['move_trigger']
    trade_period = response['trade_period']
    hour_offset = response['hour_offset']

except Exception as e:
    base = base + '/parameters'
    response = requests.get(base)
    response = response.json()
    raise Exception('No "parameters" file', response)
print(ticker, move_trigger, trade_period, hour_offset)

## Set stockObj for data
global stockObj
stockObj = Stock(ticker, token=iexkey)


logging.basicConfig(filename= '{}/subtrader.log'.format(dir_path), level=logging.DEBUG)
logger = logging.getLogger('subtrader')

class alpaca:
    def __init__(self):
        self.api = tradeapi.REST(
                        alpacaKey,
                        alpacaSecretKey,
                        'https://paper-api.alpaca.markets')
        self.account = self.api.get_account()

    def longmarket(self, ticker, shares):
        print('Going long!')
        try:
            self.api.submit_order(symbol = ticker, qty = shares, 
                side = 'buy', type = 'market', time_in_force = 'gtc')
            print('Order confirmed.') 
            time.sleep(3)
            if int(self.position(ticker).qty) > 0:
                print(f'Long position open for {ticker}')
        except Exception as e:
            # LOG HERE
            logger.error(str(e))
            print(str(e))
            print('Long market order failed.')

    def short(self, ticker, shares):
        print('Going short!')
        try: 
            self.api.submit_order(symbol = ticker, qty = shares, side = 'sell', type = 'market', time_in_force = 'gtc')
            time.sleep(4)
            print('Order confirmed.')
            
            if int(self.position(ticker).qty) < 0:
                print(f'Short position open for {ticker}')
        except Exception as e:
            logger.error(str(e))
            print(str(e))
            print('Short order failed.')

    def checkbal(self):
        cur_bal = float(self.account.equity)
        #balance_change = float(account.equity) - float(account.last_equity)
        return cur_bal #, balance_change

    def checkMarket(self):
        clock = self.api.get_clock()
        return clock.is_open
    def checkbuyingpower(self):
        cur_bp = float(self.account.buying_power)
        return cur_bp


    def position(self, ticker):
        try:
            pos = self.api.get_position(ticker)
            print(f'Number of shares: {pos.qty}\n Market Value: {pos.market_value}\nProfit/Loss: {pos.change_today}' ) 
            return pos
        except Exception as e:
            logger.error(str(e))
            print(str(e))
            print('No position found.')


    def closeposition(self, tradeInfo):
        ticker = tradeInfo[1]
        typetoclose = tradeInfo[2]
        numshares = tradeInfo[3]
        
        print('Closing position...')
        if typetoclose == 'short':
            self.api.submit_order(symbol = ticker, qty = -int(numshares), 
                side = 'buy', type = 'market', time_in_force = 'gtc')
            time.sleep(3)
            try: 
                if self.position() == 0:
                    print("Position didn't close")
            except Exception as e:
                logger.error(str(e))
            
                print(f'Short position in {ticker} closed.')
                
        if typetoclose == 'long':
            self.api.submit_order(symbol = ticker, qty = int(numshares), 
                side = 'sell', type = 'market', time_in_force = 'gtc')
            
            time.sleep(3)
            try:
                if self.position() == 0:
                    print("Position didn't close")
                    
            except Exception as e:
                logger.error(str(e))
        

                print(f'Long position in {ticker} closed.')


def numshares(ticker):
    risk_factor = .01 # 1% of account per trade
    api = alpaca()
    balance = api.checkbal()
    buyingpower = api.checkbuyingpower()

    equity_at_risk =  350 #risk_factor*balance

    percent_risk = .02 # % of stock price

    quote = stockObj.get_quote()
    close = quote['iexRealtimePrice']
    cents_at_risk = .02*close
   
    numshares = round(equity_at_risk/cents_at_risk)
    if numshares*close > buyingpower:
        numshares = round(buyingpower/close) - 5 # subtract 5 shares to ensure enough equity...

    return numshares

def tradeInfoCreator(tradeType, tradeID):

    info_main = [tradeID, ticker, tradeType, numshares(ticker)]

    info = [str(item) for item in info_main]
    info = ','.join(info)
    info = info + '\n'
    
    
    datafile = dir_path + '/tradeIDs'
    with open(datafile, 'a') as file:
        file.writelines(info)
    
    return info_main



def long(tradeID, pct_change):
    # SETUP

    datafile = dir_path + '/data'
    base = "https://oil-trader-api.herokuapp.com/futures/realtime"
    tradeType = 'long'
    tradeInfo = tradeInfoCreator(tradeType, tradeID)
    quote = stockObj.get_quote()
    entered_price = quote['iexRealtimePrice']
    entered_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(quote['iexCloseTime']/1000 + 60*60*hour_offset))
    api = alpaca()
    numshares = tradeInfo[3]
    if numshares <= 0:
        print('Not enough buying power')
        exit()
    if api.checkMarket() == False:
        print('market closed')
        exit()
    # alpaca trading
    
    api.longmarket(ticker, tradeInfo[3])
    time.sleep(2)
    # end

    while True:
  
        
        # non-alpaca trading
        quote = stockObj.get_quote()
        current_close = quote['iexRealtimePrice']


        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(quote['iexCloseTime']/1000 + 60*60*hour_offset))

        trade_gain_or_loss = (current_close - entered_price)/entered_price
        close_reason = 'null'
        ## non-alpaca paper trading
        line = [tradeID, ticker, tradeType, pct_change, entered_price,  entered_time, current_close,current_time, trade_gain_or_loss, close_reason]
        writetodatafile(line)
        ## end

        if (trade_gain_or_loss < -.02) or (trade_gain_or_loss > .02):
            close_reason = 'stop_loss'
            line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]
            writetodatafile(line)
            api.closeposition(tradeInfo)
            time.sleep(2)
            print('killed trade ', tradeID)
            exit()

        if trade_period == 'day' and timecheck(quote) == True:
            close_reason = 'day_end'
            line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]
            writetodatafile(line)
            api.closeposition(tradeInfo)
            time.sleep(2)
            print('killed trade ', tradeID)
            exit()

        time.sleep(60)



def short(tradeID, pct_change):
    # SETUP

    base = "https://oil-trader-api.herokuapp.com/futures/realtime"
    tradeType = 'short'
    tradeInfo = tradeInfoCreator(tradeType, tradeID)
    quote = stockObj.get_quote()
    entered_price = quote['iexRealtimePrice']
    entered_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(quote['iexCloseTime']/1000 + 60*60*hour_offset))
    

    numshares = tradeInfo[3]
   
    if numshares <= 0:
        print('Not enough buying power')
        exit()
    # alpaca trading
    api = alpaca()
    if api.checkMarket() == False:
        print('market closed')
        exit()
    api.short(ticker, numshares)


    while True:
        
        quote = stockObj.get_quote()
        current_close = quote['iexRealtimePrice']
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(quote['iexCloseTime']/1000 + 60*60*hour_offset))
        
        trade_gain_or_loss = (entered_price-current_close)/entered_price
        close_reason = 'null'
        

        line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]
        

        ## checks to see if the stop loss was hit
        if (trade_gain_or_loss < -.02) or (trade_gain_or_loss > .02):
            close_reason = 'stop_loss'
            line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]
            writetodatafile(line)
            api.closeposition(tradeInfo)
            time.sleep(2)
            print('killed trade ', tradeID)
            exit()
        
        
        ## checks to see if 
        if trade_period == 'day' and timecheck(quote) == True:
            close_reason = 'day_end'
            line = [tradeID, ticker, tradeType, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason]
            writetodatafile(line)
            api.closeposition(tradeInfo)
            time.sleep(2)
            print('killed trade ', tradeID)
            exit()

        time.sleep(60)

def writetodatafile(line):
    # line is a list input
    base = "https://oil-trader-api.herokuapp.com"
    base = base + "/trades"
    obj = {'trade_id': line['tradeID'], 'ticker':line['ticker'], 'trade_type': line['tradeType'], 'pct_change': line['pct_change'], 'entered_price': line['entered_price'], 'entered_time': line['entered_time'], 'current_close': line['current_close'], 'current_time': line['current_time'], 'trade_gain_or_loss': line['trade_gain_or_loss'], 'close_reason': line['close_reason']}
    response = requests.post(base, data=obj)
    print(response.text)

def timecheck(quote):
    current_close = quote['iexRealtimePrice']
    current_time = datetime.fromtimestamp(quote['iexCloseTime']/1000 + 60*60*hour_offset).time()
    end_of_day = dt.time(15,57)

    if current_time > end_of_day:
        return True
    else:
        return False

