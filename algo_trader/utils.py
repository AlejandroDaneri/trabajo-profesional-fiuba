from lib.indicators.crossing import Crossing
from lib.indicators.rsi import RSI
from lib.strategies.basic import Basic

def hydrate_indicator_rsi(parameters):
    if parameters is None:
        print("indicator rsi not have parameters")
        return None
    buy_threshold = parameters["buy_threshold"]
    sell_threshold = parameters["sell_threshold"]
    rounds = parameters["rounds"]
    if buy_threshold is None or sell_threshold is None or rounds is None:
        print("indicator rsi not have all the parameters")
        return None
    return RSI(buy_threshold, sell_threshold, rounds)

def hydrate_indicator_crossing(parameters):
    if parameters is None:
        print("indicator crossing not have parameters")
        return None
    buy_threshold = parameters["buy_threshold"]
    sell_threshold = parameters["sell_threshold"]
    fast = parameters["fast"]
    slow = parameters["slow"]
    if buy_threshold is None or sell_threshold is None or fast is None or slow is None:
        print("indicator crossing not have all the parameters")
        return None
    return Crossing(buy_threshold, sell_threshold, fast, slow)

def hydrate_strategy(currencies, indicators):
    strategy = {}
    for currency in currencies:
        indicators_builded = []

        for indicator in indicators:
            if indicator["name"] == "rsi":
                rsi = hydrate_indicator_rsi(indicator["parameters"])
                if rsi is not None:
                    indicators_builded.append(rsi)

            elif indicator["name"] == "crossing":
                crossing = hydrate_indicator_crossing(indicator["parameters"])
                if crossing is not None:
                    indicators_builded.append(crossing)
        
        strategy[currency] = Basic(indicators_builded)
    return strategy