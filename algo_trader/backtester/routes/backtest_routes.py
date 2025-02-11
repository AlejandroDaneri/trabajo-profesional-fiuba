from datetime import datetime, timezone
from lib.utils.plotter import buy_and_hold_balance_series, trades_2_balance_series
from lib.providers.binance import Binance
from lib.providers.yahoofinance import YahooFinance
from config import make_cache_key
from flask import Blueprint, jsonify, request, abort
from services.data_service import get_data
from services.risk_service import RiskCalculator
from executors.buy_and_hold import BuyAndHoldBacktester
from executors.futures_backtester import FuturesBacktester
from executors.spot_backtester import SpotBacktester
from lib.utils.utils_backtest import hydrate_strategy
from lib.constants.timeframe import DATE_FORMAT, TIMEFRAME_1_DAY
from config import cache
import pandas as pd
backtest_blueprint = Blueprint('backtest', __name__)

@backtest_blueprint.route('/backtest', methods=['POST'])
@cache.memoize(timeout=3600, make_name=make_cache_key)
def backtest():
    print("[Backtester] a new backtest was requested")
    req_data = request.get_json()
    if not req_data:
        abort(400, description="JSON data is missing in the request body.")

    required_params = ['coins', 'initial_balance', 'data_from', 'data_to', 'timeframe', 'indicators','strategy','type']
    missing_params = [param for param in required_params if param not in req_data]
    if missing_params:
        abort(400, description=f"Required parameters {missing_params} are missing in the JSON data.")

    coins = req_data['coins']
    initial_balance = req_data['initial_balance']
    data_from_ts = req_data['data_from']
    data_to_ts = req_data['data_to']
    timeframe = req_data['timeframe']
    indicators = req_data['indicators']
    strategy_id = req_data['strategy']
    data_from = datetime.fromtimestamp(int(data_from_ts), tz=timezone.utc).strftime(DATE_FORMAT[timeframe])
    data_to = datetime.fromtimestamp(int(data_to_ts), tz=timezone.utc).strftime(DATE_FORMAT[timeframe])
    backtest_type = req_data['type']
    try:
        initial_balance = float(initial_balance)
    except ValueError:
        abort(400, description="'initial_balance' must be a valid number.")

    results = {}
    for coin in coins:

        provider = Binance()

        print("[Backtester] getting data: started")

        cache_key = f"data_{coin}_{timeframe}"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            print(cache_key)
            # If data is not in cache, save it
            data = provider.get(coin, timeframe, data_from, data_to)
            cache.set(cache_key, data)
        else:
            # If data is in cache, use it
            cached_data_from = cached_data.index[0]
            cached_data_to = cached_data.index[-1]

            if cached_data_from <= data_from and cached_data_to >= data_to:
                # If requested data is a subset of cache
                data = cached_data.loc[data_from:data_to]
            else:
                # If requested data need more data than cached
                new_data_from = min(data_from, cached_data_from)
                new_data_to = max(data_to, cached_data_to)
                new_data = provider.get(coin, timeframe, new_data_from, new_data_to)
                cache.set(cache_key, new_data)
                data = new_data.loc[data_from:data_to]

        if data.empty:
            abort(500, description=f"Failed request to YFinance for {coin}")
        print("[Backtester] getting data: finished")

        strategy = hydrate_strategy([coin], indicators, timeframe, strategy_id)
        if backtest_type == 'spot':
            backtester = SpotBacktester(strategy[coin], initial_balance)
        elif backtest_type == 'futures':
            backtester = FuturesBacktester(strategy[coin], initial_balance)
        else: 
            abort(400, description="'type' is not valid.")


        print("[Backtester] backtest: started")
        trades, final_balance = backtester.execute(data)
        print("[Backtester] backtest: finished")

        byh_backtester = BuyAndHoldBacktester(initial_balance, data)
        byh_backtester.backtest()

        
        risks = {}
        buy_and_hold_metrics = RiskCalculator(byh_backtester.log_returns, byh_backtester.linear_returns)
        buy_and_hold = buy_and_hold_metrics.calculate()

        strategy_metrics = RiskCalculator(backtester.log_returns, backtester.linear_returns)
        strategy_risks = strategy_metrics.calculate()
        
        risks["buy_and_hold"] = buy_and_hold
        risks["strategy"] = strategy_risks

        print("[Backtester] building strategy series: started")
        strategy_balance_series = trades_2_balance_series(data, trades, timeframe, initial_balance)
        print("[Backtester] building strategy series: finished")

        print("[Backtester] building buy and hold series: started")
        hold_balance_series = buy_and_hold_balance_series(data, timeframe, initial_balance)
        print("[Backtester] building buy and hold series: finished")

        df_series = pd.merge(strategy_balance_series, hold_balance_series, on='date', how='outer', suffixes=('_strategy', '_buy_and_hold'))
        results[coin] = { 
            'trades': trades.to_dict(orient='records'), 
            'risks':risks,
            'series': df_series.to_dict(orient='records'),
            'final_balance': df_series.tail(1)["balance_strategy"].values[0]
        }

    return jsonify(results)