# **API**
## Energy Equities Trading Algo
### for Hamilton Miller Investments

Features
- Hosted on Heroku
- API stucture for "get", "post", and "delete" methods
- Also, running background process called "data_reader" that posts oil futures data to the API

Important Details
- Timezone is in **EST**
    - So, if you GET, the time will be in **EST**
    - If you POST, make sure to POST in **EST**!
```
timeformat = "%Y-%m-%d %H:%M:%S"
```
### **GET Usage**

For real-time (minute bars) data:
```
base = "https://oil-trader-api.herokuapp.com/futures/realtime"
response = requests.get(base)
response = response.json()
close = response['close']
times = response['time']
print(response)

```
For historical data:

```
base = "https://oil-trader-api.herokuapp.com/futures/historical"
response = requests.get(base)
response = response.json()
close = response['closes']
times = response['times']
print(response)

```
This will give ALL data registered in the CSV file from the APP.py


# To Do's/Task List
- [ ] Implement SQL databasing
- _Estimated: 12/30/2020_

# HEROKU PUSHING
1) Make sure to be in "oil-trader" directory directly over API files
and enter into env via:
```
$ source env/bin/activate
```
2) 
```
$ git add .
```
3) 
```
$ git commit -am "some commit message"
```
4)
```
$ git push heroku master
```

OTHER

```
# To login:
$ heroku login

#Clone the repository
#Use Git to clone oil-api's source code to your local machine.
$ heroku git:clone -a oil-api
$ cd oil-api
```
