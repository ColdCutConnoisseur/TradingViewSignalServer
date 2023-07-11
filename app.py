"""Main Webapp serving as API"""

import os
import time
from datetime import datetime

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:////' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TradeSignal(db.Model):
    __tablename__ = 'trade_signals'
    id = db.Column(db.Integer, primary_key=True) # Timestamp
    trade_date = db.Column(db.Date)
    asset = db.Column(db.String(64))
    side = db.Column(db.String(64))
    action = db.Column(db.String(64))

@app.route('/')
def index():
    # TODO: Add dashboard showing signals from db
    return '<h1>Welcome Darwish!</h1>'

@app.route('/add_new_signal', methods=['POST'])
def add_signal_to_database():
    #content_type = request.headers.get('Content-Type')

    #if content_type == "application/json":
    json_content = request.json

    trade_id = int(time.time())
    #trade_date = json_content['timestamp']
    trade_date = datetime.today()
    trade_asset = json_content['asset']
    trade_side = json_content['side']
    trade_action = json_content['action']

    new_signal = TradeSignal(
                    id=trade_id,
                    trade_date=trade_date,
                    asset=trade_asset,
                    side=trade_side,
                    action=trade_action
                    )
    db.session.add(new_signal)
    db.session.commit()

    return 'New Signal Successfully Committed!'

@app.route('/get_todays_signals', methods=['GET'])
def get_todays_signals():
    todays_date = datetime.today()
    todays_signals = TradeSignal.query.filter_by(trade_date=todays_date).all()
    return todays_signals

@app.route('/get_last_n_signals/<num_signals>', methods=['GET'])
def get_last_n_signals(num_signals):
    n_signals = min(int(num_signals), 25)

    last_signals = TradeSignal.query.order_by(TradeSignal.trade_date).all()

    return_signals = last_signals[:n_signals]

    return_dict = {}

    for num, sig in enumerate(return_signals):
        new_key = "Signal" + str(num)

        new_val = [sig.id, sig.trade_date, sig.asset, sig.side, sig.action]

        return_dict[new_key] = new_val

    return return_dict
