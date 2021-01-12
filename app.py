#!flask/bin/python
from flask import Flask, request, jsonify

from databaser import addClose
from databaser import reader
from databaser import deleteLast
from databaser import historicals
app = Flask(__name__)


@app.route("/futures/realtime", methods=["GET"])
def message():
    time, close = reader()
    return {'time': time, 'close': close}

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
        update =  addClose(time, close)
        return jsonify(str(update))


@app.route("/futures", methods=["DELETE"])
def delete():
    if request.method=='DELETE':
        delete_message =  deleteLast()
        return jsonify(str(delete_message))

if __name__ == '__main__':
    app.run(debug=True)

