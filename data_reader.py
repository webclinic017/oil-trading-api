from bs4 import BeautifulSoup 
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import time
from datetime import date, datetime, timedelta
import os
import sys

dir_path = os.path.dirname(__file__)
timeformat = "%Y-%m-%d %H:%M:%S"
MST_to_EST = timedelta(hours = -5)
url = 'https://www.investing.com/commodities/crude-oil-historical-data'
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'}
base = "https://oil-api.herokuapp.com/futures"

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def futures_data_reader():
    try:
        source = requests.get(url, headers=headers, timeout = 1.5)
        source.encoding = 'utf-8' 
        status = source.status_code
        source = source.text
        soup =  BeautifulSoup(source, 'html.parser')
        divs = soup.find("div", {"id": "quotes_summary_current_data"})
        price = divs.find('span').text
        price = price.strip("'")
        price = float(price)
        now = (datetime.now() + MST_to_EST).strftime(timeformat)

        data_obj = {'time': now, 'close': price}
    except Exception as e:
        sys.stdout.write(str(e))
        now = (datetime.now() + MST_to_EST).strftime(timeformat)
        data_obj = {'time': now, 'close': 'NaN'}


    try:
        response = requests.post(base, data=data_obj, timeout=1.5)
    except Exception as e:
        sys.stdout.write(str(e))

        

    
sched.start()