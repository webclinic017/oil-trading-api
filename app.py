#!flask/bin/python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from databaser import addClose
from databaser import reader
from databaser import deleteLast
from databaser import historicals
app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:1234/postgres'

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fgbuqcuqjvjptf:22441a869f92567a97c366cbc7204aa3cd58cc7b068e68b65f07c6161b8da03b@ec2-54-159-138-67.compute-1.amazonaws.com:5432/d8th6a2gl59nj0'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String)
    price = db.Column(db.Float)
    
    
    def __init__(self,time, price):
        self.time = time
        self.price = price

    # add line here for ticker!

  


@app.route("/futures/realtime", methods=["GET"])
def message():
    record = db.session.query(Data).order_by(Data.id.desc()).first()

    #time, close = reader()
    return {'time': str(record), 'close': str(record)}

@app.route("/futures/historical", methods=["GET"])
def historical():
    times, closes = historicals()
    return {'times': list(times), 'closes': list(closes)}

@app.route("/futures", methods=["POST"])
def post():
    if request.method=='POST':
        print('post')
        close = request.form['close']
        print(close)
        time = request.form['time']
        #update =  addClose(time, close)

        ## databasing
        print(time, close)

        data = Data(time, close)
        db.session.add(data)
        db.session.commit()

        return jsonify(str('yes'))


@app.route("/futures", methods=["DELETE"])
def delete():
    if request.method=='DELETE':
        delete_message =  deleteLast()
        return jsonify(str(delete_message))

if __name__ == '__main__':
    app.run(debug=True)

