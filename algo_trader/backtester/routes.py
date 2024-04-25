from flask import Flask, jsonify, request, abort
from datetime import datetime,timezone  
from trading_logic import getData, getFeatures, getActions, getTrades, eventDriveLong

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

@app.route('/ping')
def ping():
    return "ok", 200

@app.route('/backtest')
def backtest():
    coin = request.args.get('coin')
    initial_balance = request.args.get('initial_balance')
    data_from_ts = request.args.get('data_from')
    data_to_ts = request.args.get('data_to')

    if not (coin and initial_balance and data_from_ts and data_to_ts):
        abort(400, description="Required parameters 'coin', 'initial_balance', 'data_from', or 'data_to' are missing in the URL.")
    data_from = datetime.fromtimestamp(int(data_from_ts), tz=timezone.utc).strftime('%Y-%m-%d')
    data_to = datetime.fromtimestamp(int(data_to_ts), tz=timezone.utc).strftime('%Y-%m-%d')

    try:
        initial_balance = float(initial_balance)
    except ValueError:
        abort(400, description="'initial_balance' must be a valid number.")

    data = getData(ticker=coin +'-USD', data_from=data_from, data_to=data_to)
    features = getFeatures(data, n_obv=100, n_sigma=40, n_rsi=15, fast=20, slow=60)
    actions = getActions(data, features, 0, 65, 0.01, -0.01, 55, 0)
    trades = getTrades(actions)
    payoff = eventDriveLong(data)
    results = payoff.iloc[:,-2:].add(1).cumprod()

    trades_dict = trades.to_dict(orient='records')
    results_dict = results.to_dict(orient='records') #comparing vs buy and hold

    response_dict = {
        'trades': trades_dict, # comento por ahora nomas para que no me rompa golang
        'results_dict': results_dict, # comento por ahora nomas para que no me rompa golang
        'final_balance' : str(initial_balance * (1 + trades['rendimientoAcumulado']).iloc[-1]) if len(trades)>0 else "no trades, WIP"

    }

    return jsonify(response_dict)
    
