from flask import Flask, jsonify


app = Flask(__name__)
from trading_logic import getData, getFeatures, getActions, getTrades


@app.route('/backtest')
def hello_world():
    data = getData(ticker='SOL-USD', data_from='2021-01-01', data_to='2023-05-05')
    features = getFeatures(data, n_obv=100, n_sigma=40, n_rsi=15, fast=20, slow=60)
    actions = getActions(data, features, 0, 65, 0.01, -0.01, 55, 0)
    trades = getTrades(actions)
    trades_dict = trades.to_dict(orient='records')
    
    return jsonify(trades_dict)
    
