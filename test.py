#!flask/bin/python
import requests
import os
import json 
base = "https://oil-trader-api.herokuapp.com/futures"
#base = 'http://127.0.0.1:5000/futures/historical'
obj = {'time': '2019-02-01 19:55', 'close': 555.00}
response = requests.post(base, data=obj)
# print(response.text)
response = requests.get(base)
# #response = requests.delete(base) #, data=obj)
print(response)


