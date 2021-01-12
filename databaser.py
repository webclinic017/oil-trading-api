import pandas as pd 
import os 
import os


dir_path = os.path.dirname(__file__)
# DATABASE_URL = os.environ['postgres://cxpvtixpnetcit:40da0e193387863bf71adfcfd10e80242b5818a273ec96ce9aef0c2b801815f6@ec2-54-158-190-214.compute-1.amazonaws.com:5432/d6rjv08pb6aa4c']

# conn = psycopg2.connect(DATABASE_URL, sslmode='require')


def addClose(time, close):
    isThere = False

    df1 = pd.read_csv(dir_path+"/futures_data.csv")

    try:
        close = float(close)
        time = time


    except ValueError:
        error = "error"
        return error


    # Creating the Second Dataframe using dictionary 

    if isThere != True: 

        df2 = pd.DataFrame.from_dict({'time':[time], 'close':[close]}) 

        dff = df1.append(df2, ignore_index = True)
        dff.to_csv(dir_path+'/futures_data.csv', index = False)
        add = 'added'
        return add

    else:
        df1.to_csv(dir_path+'/futures_data.csv', index = False) 
        update = 'updated'
        return update


def reader():
    df1 = pd.read_csv(dir_path+"/futures_data.csv")
    time = df1['time'].values[-1]
    close = df1['close'].values[-1]
    return time, float(close)


def deleteLast():
    df1 = pd.read_csv(dir_path+"/futures_data.csv")
    try:
        df1.drop(df1.tail(1).index,inplace=True)
        df1.to_csv(dir_path+"/futures_data.csv")
        return "deleted last row"
    except Exception as e:
        return str(e)

def historicals():
    df1 = pd.read_csv(dir_path+"/futures_data.csv")
    times = df1['time'].values

    closes = df1['close'].values

    return times, closes


