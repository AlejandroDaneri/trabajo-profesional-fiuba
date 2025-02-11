from lib.indicators import *
from lib.strategies.strategy import Strategy
from lib.strategies.RLstrategy import RL
from lib.strategies.LSTMstrategy import LSTM
from lib.strategies.TDstrategy import TDstrategy
from lib.strategies.basic import Basic
from typing import Dict

def hydrate_strategy(type, currencies, indicators, timeframe, id) -> Dict[str, Strategy]:
    strategy = {}
    for currency in currencies:
        indicators_builded = []

        for indicator in indicators:
            indicator_name = indicator["name"]
            indicator_params = indicator["parameters"]
            
            indicator_class = globals().get(indicator_name)
            if indicator_class is None:
                print(f"Indicator {indicator_name} not found.")
                continue
            
            instance = indicator_class.hydrate(indicator_params)
            if instance is not None:
                indicators_builded.append(instance)

        if type == "basic" or type == "":
            strategy[currency] = Basic(indicators_builded, timeframe, id)
        elif type == "rl":
            strategy[currency] = RL(indicators_builded, timeframe, id)
        elif type == "lstm":
            strategy[currency] = LSTM(indicators_builded, timeframe, id)
        elif type == "td":
            strategy[currency] = TDstrategy(indicators_builded, timeframe, id)

    return strategy


def timeframe_2_seconds(timeframe) -> int:
    if timeframe == "1m":
        return 60
    elif timeframe == "5m":
        return 60 * 5
    elif timeframe == "15m":
        return 60 * 15
    elif timeframe == "30m":
        return 60 * 30
    elif timeframe == "1h":
        return 60 * 60
    elif timeframe == "4h":
        return 60 * 60 * 4
    elif timeframe == "1d":
        return 60 * 60 * 24
    else:
        # default 1m
        print("[utils] invalid timeframe, using default => 1 minute")
        return 60
