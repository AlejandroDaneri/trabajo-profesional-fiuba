from flask import Flask, jsonify, request
from datetime import datetime,timezone
from trading_logic import getData, getFeatures, getActions, getTrades, eventDriveLong

app = Flask(__name__)


@app.route('/backtest')
def hello_world():
    coin = request.args.get('coin', 'SOL') 
    initial_balance = float(request.args.get('initial_balance', 1000.0))  
    data_from_ts = request.args.get('data_from', None)
    data_to_ts = request.args.get('data_to', None)

    if data_from_ts is not None:
        data_from = datetime.fromtimestamp(int(data_from_ts),tz=timezone.utc).strftime('%Y-%m-%d')
    else:
        data_from = '2021-01-01'  

    if data_to_ts is not None:
        data_to = datetime.fromtimestamp(int(data_from_ts),tz=timezone.utc).strftime('%Y-%m-%d')
    else:
        data_to = '2023-05-05'  


    data = getData(ticker=coin +'-USD', data_from=data_from, data_to=data_to)
    features = getFeatures(data, n_obv=100, n_sigma=40, n_rsi=15, fast=20, slow=60)
    actions = getActions(data, features, 0, 65, 0.01, -0.01, 55, 0)
    trades = getTrades(actions)
    payoff = eventDriveLong(data)
    results = payoff.iloc[:,-2:].add(1).cumprod()

    trades_dict = trades.to_dict(orient='records')
    results_dict = results.to_dict(orient='records') #comparing vs buy and hold
    response_dict = {
        'trades': trades_dict, ## trades realized
        'benchmarking': results_dict, ## comparing to buy and hold
        'final_balance' : initial_balance * (1 + trades['rendimientoAcumulado']).iloc[-1]

    }

    # Devolver el diccionario como respuesta JSON
    return jsonify(response_dict)
    
