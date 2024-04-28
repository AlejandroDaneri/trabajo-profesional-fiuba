from lib.utils.utils_backtest import hydrate_strategy
from flask import Flask, jsonify, request, abort
from datetime import datetime,timezone  
from trading_logic import calculateFinalBalance, getData, getFeatures, getActions, getTrades, eventDriveLong
import logging
app = Flask(__name__)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': error.description}), 500

@app.route('/ping')
def ping():
    return "ok", 200

@app.route('/backtest', methods=['POST'])
def backtest():
    req_data = request.get_json()
    if not req_data:
        abort(400, description="JSON data is missing in the request body.")

    required_params = ['coins', 'initial_balance', 'data_from', 'data_to', 'timeframe', 'indicators']
    missing_params = [param for param in required_params if param not in req_data]
    if missing_params:
        abort(400, description=f"Required parameters {missing_params} are missing in the JSON data.")

    coins = req_data['coins']
    initial_balance = req_data['initial_balance']
    data_from_ts = req_data['data_from']
    data_to_ts = req_data['data_to']
    timeframe = req_data['timeframe']
    indicators = req_data['indicators']

    data_from = datetime.fromtimestamp(int(data_from_ts), tz=timezone.utc).strftime('%Y-%m-%d')
    data_to = datetime.fromtimestamp(int(data_to_ts), tz=timezone.utc).strftime('%Y-%m-%d')

    try:
        initial_balance = float(initial_balance)
    except ValueError:
        abort(400, description="'initial_balance' must be a valid number.")
    timeframe_mapping = {
        '1M': '1mo',
        '1D': '1d',
        '1W': '1wk',
        '5D': '5d',
        '1H': '1h',
        '60m': '60m',
        '30m': '30m',
        '15m': '15m',
        '5m': '5m',
        '2m': '2m',
        '1m': '1m',
        '90m': '90m',
        '3M': '3mo'
    }
    if timeframe not in timeframe_mapping:
        return abort(400, description="Invalida timeframe.")
    results = {}
    for coin in coins:
        data = getData(ticker=coin + '-USD', data_from=data_from, data_to=data_to, timeframe=timeframe_mapping[timeframe])
        if data.empty:
            abort(500, description=f"Failed request to YFinance for {coin}")
        
        strategy = hydrate_strategy([coin], indicators, timeframe, 123)  # FIXME: Not sure how to get strategy
        trades = strategy[coin].backtest(data)

        final_balance = initial_balance * (1 + trades['cumulative_return']).iloc[-1] if len(trades) > 0 else 0
        results[coin] = {'final_balance': final_balance}
    # data = getData(ticker=coin +'-USD', data_from=data_from, data_to=data_to,timeframe = timeframe_mapping[timeframe])
    # if(data.empty):
    #     abort(500, description="Failed request to YFinance")   
    # strategy = hydrate_strategy([coin], indicators, timeframe, 123) ## FIXME

    # trades = strategy[coin].backtest(data)
    # features = getFeatures(data, n_obv=100, n_sigma=40, n_rsi=15, fast=20, slow=60)
    # actions = getActions(data, features, 0, 65, 0.01, -0.01, 55, 0)
    # trades = getTrades(actions)
    # payoff = eventDriveLong(data)
    # results = payoff.iloc[:,-2:].add(1).cumprod()
    # final_balance = calculateFinalBalance(data,trades,initial_balance)
    # trades_dict = trades.to_dict(orient='records')
    # results_dict = results.to_dict(orient='records') #comparing vs buy and hold

    response_dict = {
        #'trades': trades_dict,  comento por ahora nomas para que no me rompa golang
        #'results_dict': results_dict,  comento por ahora nomas para que no me rompa golang
        'final_balance' : initial_balance * (1 + trades['cumulative_return']).iloc[-1] if len(trades)>0 else 0

    }

    return jsonify(results)
    
