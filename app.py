#!flask/bin/python
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost' #postgres:postgres@localhost:5432/postgres'

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://yhrlvfsgkycmqh:52670716d15893538fd1e5c02ff8316180f977cbcef7302df87bab818b93eba6@ec2-18-205-122-145.compute-1.amazonaws.com:5432/dbr7bs13kg83jn'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *

try:
    db.create_all()
except:
    print('Tables exist already.')


@app.route("/futures/realtime", methods=["GET"])
def message():
    try:
        record = db.session.query(Data).order_by(Data.id.desc()).first()
        record = record.__dict__
        print(record)
        return {'time': record['time'], 'close': record['close']}
    except Exception as e:
        print(str(e))
        return {'time': 'none', 'close': 'none'}
    

@app.route("/futures/historical", methods=["GET"])
def historical():
    records = db.session.query(Data).all()
    times, closes = [], []
    for data in records:
        data = data.__dict__
        times.append(data['time'])
        closes.append(data['close'])

    return {'times': list(times), 'closes': list(closes)}


@app.route("/futures", methods=["POST"])
def post():
    if request.method=='POST':
        print('post')
        close = request.form['close']
        print(close)
        time = request.form['time']
        print(time, close)

        data = Data(time, close)
        db.session.add(data)
        db.session.commit()

        return jsonify({'time':time, 'close':close})



@app.route("/parameters", methods=["GET"])
def params_get():
    record = AlgoParameters.query.all()
    data = vars(record[-1])

    ticker = data['ticker']
    move_trigger = data['move_trigger']
    trade_period = data['trade_period']
    hour_offset = data['hour_offset']
 
    return {'ticker': ticker, 'move_trigger': move_trigger, 'trade_period': trade_period, 'hour_offset': hour_offset}


@app.route("/parameters", methods=["POST"])
def params_post():
    if request.method=='POST':
        print('post')
        ticker = request.form['ticker']
        move_trigger = request.form['move_trigger']
        trade_period = request.form['trade_period']
        hour_offset = request.form['hour_offset']

        data = AlgoParameters(ticker, move_trigger, trade_period, hour_offset)
        db.session.query(AlgoParameters).delete()
        db.session.add(data)
        db.session.commit()

        return jsonify({'ticker':ticker, 'move_trigger': move_trigger, 'trade_period': trade_period, 'hour_offset': hour_offset})


@app.route("/trades", methods=["GET"])
def trades_get():
    records = db.session.query(Trades).all()
    trade_id, ticker, trade_type, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason = ([] for i in range(10))
    for data in records:
        data = vars(data)
        trade_id.append(data['trade_id'])
        ticker.append(data['ticker'])
        trade_type.append(data['trade_type'])
        pct_change.append(data['pct_change'])
        entered_price.append(data['entered_price'])
        entered_time.append(data['entered_time'])
        current_close.append(data['current_close'])
        current_time.append(data['current_time'])
        trade_gain_or_loss.append(data['trade_gain_or_loss'])
        close_reason.append(data['close_reason'])

    return {'trade_id':trade_id, 'ticker': list(ticker), 'trade_type': list(trade_type), 'pct_change': list(pct_change), 'entered_price': list(entered_price), 'current_close':list(current_close), 'current_time': list(current_time), 'trade_gain_or_loss': list(trade_gain_or_loss), 'close_reason': list(close_reason)}


@app.route("/trades", methods=["POST"])
def trades_post():
    if request.method=='POST':
        trade_id = request.form['trade_id']
        ticker = request.form['ticker']
        trade_type = request.form['trade_type']
        pct_change = request.form['pct_change']
        entered_price = request.form['entered_price']
        entered_time = request.form['entered_time']
        current_close = request.form['current_close']
        current_time = request.form['current_time']
        trade_gain_or_loss = request.form['trade_gain_or_loss']
        close_reason = request.form['close_reason']

        data = Trades(trade_id, ticker, trade_type, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason)
        
        db.session.add(data)
        db.session.commit()

        return jsonify({'trade_id':trade_id, 'ticker':ticker, 'trade_type': trade_type, 'pct_change': pct_change, 'entered_price': entered_price, 'entered_time': entered_time, 'current_close': current_close, 'current_time':current_time, 'trade_gain_or_loss': trade_gain_or_loss, 'close_reason': close_reason})


# @app.route("/trades/view", methods=["GET"])
# def view_trades():
#     return render_template(
#       'users.jinja2',
#         users=User.query.all(),
#         title="Show Users"
#     )

if __name__ == '__main__':
    app.run(debug=True)

