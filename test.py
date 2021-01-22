#!flask/bin/python
import requests
import os
import json 
import pandas as pd

base = "https://oil-trader-api.herokuapp.com/futures/historical"
#base = 'http://127.0.0.1:5000/futures/historical'
#obj = {'time': '2019-02-01 19:55', 'close': 555.00}
#response = requests.post(base, data=obj)
# print(response.text)
response = requests.get(base)
# #response = requests.delete(base) #, data=obj)
data = response.json()
print(data)
closes = data['closes']
times = data['times']
df = pd.DataFrame.from_dict(data)
df.to_csv('/Users/noahalex/Desktop/data1.csv')

