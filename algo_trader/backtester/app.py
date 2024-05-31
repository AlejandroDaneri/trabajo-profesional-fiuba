from executors.futures_backtester import FuturesBacktester
from executors.buy_and_hold import BuyAndHoldBacktester
from executors.spot_backtester import SpotBacktester
from lib.utils.utils_backtest import hydrate_strategy
from lib.utils.plotter import trades_2_balance_series, buy_and_hold_balance_series
from lib.providers.yahoofinance import YahooFinance
from lib.providers.binance import Binance
from lib.indicators import __all__ as indicators_list
from lib.indicators import *
from lib.constants.timeframe import DATE_FORMAT, TIMEFRAME_1_DAY

from flask import Flask, jsonify, request, abort
from datetime import datetime,timezone  
import yfinance as yf
from services.risk_service import RiskCalculator
import pandas as pd

import hashlib
import json
from flask_caching import Cache
from flask import Flask
from flask_caching import Cache
from routes.backtest_routes import backtest_blueprint
from routes.indicator_routes import indicator_blueprint
from config import cache  # Import the cache object from cache.py
app = Flask(__name__)


cache.init_app(app)

app.register_blueprint(backtest_blueprint)
app.register_blueprint(indicator_blueprint)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': error.description}), 500

@app.route('/ping')
def ping():
    return "ok", 200

if __name__ == '__main__':
    app.run()
