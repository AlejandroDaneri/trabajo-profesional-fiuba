from flask import Flask, jsonify, request

app = Flask(__name__)
from trading_logic import getData, getFeatures, getActions, getTrades, eventDriveLong


@app.route('/backtest')
def hello_world():
    coin = request.args.get('coin', 'SOL') 
    initial_balance = float(request.args.get('initial_balance', 1000.0))  

    data = getData(ticker=coin +'-USD', data_from='2021-01-01', data_to='2023-05-05')
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
    
