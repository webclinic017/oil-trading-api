
import requests
import pandas as pd
base = 'http://0.0.0.0:5000'

def read_historical_data(base):
    base = base + '/futures/historical'
    response = requests.get(base)
    response = response.json()
    close = response['closes']
    times = response['times']
    df = pd.DataFrame.from_dict({"close": close, "time": times})
    print(df)

def post_data(base):
    base = base+'/futures'
    obj = {'time': '2019-02-01 19:57', 'close': 557.00}
    response = requests.post(base, data=obj)
    print(response.text)

def post_params(base):
    base = base + "/parameters"
    obj = {'ticker': 'BP', 'move_trigger': .001, 'trade_period': 'day', 'hour_offset': 5}
    response = requests.post(base, data=obj)
    print(response.text)

def post_trades(base):
    base = base + "/trades"
    obj = {'trade_id': 1, 'ticker':'xof', 'trade_type': 'win', 'pct_change': .03, 'entered_price': 10.1, 'entered_time': 'asdfasdf', 'current_close': 23.23, 'current_time':'dfdfdf', 'trade_gain_or_loss': 40.5, 'close_reason': 'yes'}
    response = requests.post(base, data=obj)
    print(response.text)

# read_historical_data(base)
#post_data(base)
#post_params(base)
post_trades(base)
