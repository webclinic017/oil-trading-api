

from app import db


class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String)
    close = db.Column(db.Float)
    
    def __init__(self,time, close):
        self.time = time
        self.close = close


class AlgoParameters(db.Model):
    __tablename__ = 'parameters'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String)
    move_trigger = db.Column(db.Float)
    trade_period = db.Column(db.String)
    hour_offset = db.Column(db.Integer)
    def __init__(self, ticker, move_trigger, trade_period, hour_offset):
        self.ticker = ticker
        self.move_trigger = move_trigger
        self.trade_period=trade_period
        self.hour_offset=hour_offset
    def as_dict(self):
         return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Trades(db.Model):
    __tablename__ = 'trades'
    id = db.Column(db.Integer, primary_key=True)
    trade_id = db.Column(db.Integer)
    ticker = db.Column(db.String)
    trade_type = db.Column(db.String)
    pct_change = db.Column(db.Float)
    entered_price = db.Column(db.Float)
    entered_time = db.Column(db.String)
    current_close = db.Column(db.Float)
    current_time = db.Column(db.String)
    trade_gain_or_loss = db.Column(db.Float)
    close_reason = db.Column(db.String)
    def __init__(self, trade_id, ticker, trade_type, pct_change, entered_price, entered_time, current_close, current_time, trade_gain_or_loss, close_reason):
        self.trade_id = trade_id
        self.ticker = ticker 
        self.trade_type = trade_type 
        self.pct_change = pct_change 
        self.entered_price = entered_price 
        self.entered_time = entered_time 
        self.current_time = current_time
        self.current_close = current_close
        self.trade_gain_or_loss = trade_gain_or_loss 
        self.close_reason = close_reason

