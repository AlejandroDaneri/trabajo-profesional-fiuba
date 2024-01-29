from lib.indicators.crossing import Crossing
from lib.indicators.rsi import RSI
from lib.indicators.macd import MACD
from lib.indicators.bbands import BBANDS
from lib.indicators.dmi import DMI
from lib.indicators.ema import EMA
from lib.indicators.sma import SMA
from lib.indicators.obv import OBV
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

def hydrate_indicator_macd(parameters):
    if parameters is None:
        print("indicator macd not have parameters")
        return None
    slow = parameters["slow"]
    fast = parameters["fast"]
    smoothed = parameters["smoothed"]
    if slow is None or fast is None or smoothed is None:
        print("indicator macd not have all the parameters")
        return None
    return MACD(slow, fast, smoothed)

def hydrate_indicator_bbands(parameters):
    if parameters is None:
        print("indicator bbands not have parameters")
        return None
    rounds = parameters["rounds"]
    factor = parameters["factor"]
    if rounds is None or factor is None:
        print("indicator bbands not have all the parameters")
        return None
    return BBANDS(rounds, factor)

def hydrate_indicator_dmi(parameters):
    if parameters is None:
        print("indicator dmi not have parameters")
        return None
    rounds = parameters["rounds"]
    adx_threshold = parameters["adx_threshold"]
    if rounds is None or adx_threshold is None:
        print("indicator dmi not have all the parameters")
        return None
    return DMI(rounds, adx_threshold)

def hydrate_indicator_ema(parameters):
    if parameters is None:
        print("indicator ema not have parameters")
        return None
    fast_rounds = parameters["fast_rounds"]
    slow_rounds = parameters["slow_rounds"]
    if fast_rounds is None or slow_rounds is None:
        print("indicator ema not have all the parameters")
        return None
    return EMA(fast_rounds, slow_rounds)

def hydrate_indicator_sma(parameters):
    if parameters is None:
        print("indicator sma not have parameters")
        return None
    fast_rounds = parameters["fast_rounds"]
    slow_rounds = parameters["slow_rounds"]
    if fast_rounds is None or slow_rounds is None:
        print("indicator sma not have all the parameters")
        return None
    return SMA(fast_rounds, slow_rounds)

def hydrate_indicator_obv(parameters):
    if parameters is None:
        print("indicator obv not have parameters")
        return None
    rounds = parameters["rounds"]
    if rounds is None:
        print("indicator obv not have all the parameters")
        return None
    return OBV(rounds)

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

            elif indicator["name"] == "macd":
                macd = hydrate_indicator_macd(indicator["parameters"])
                if macd is not None:
                    indicators_builded.append(macd)

            elif indicator["name"] == "bbands":
                bbands = hydrate_indicator_bbands(indicator["parameters"])
                if bbands is not None:
                    indicators_builded.append(bbands)

            elif indicator["name"] == "dmi":
                dmi = hydrate_indicator_dmi(indicator["parameters"])
                if dmi is not None:
                    indicators_builded.append(dmi)

            elif indicator["name"] == "ema":
                ema = hydrate_indicator_ema(indicator["parameters"])
                if ema is not None:
                    indicators_builded.append(ema)

            elif indicator["name"] == "sma":
                sma = hydrate_indicator_sma(indicator["parameters"])
                if sma is not None:
                    indicators_builded.append(sma)

            elif indicator["name"] == "obv":
                obv = hydrate_indicator_obv(indicator["parameters"])
                if obv is not None:
                    indicators_builded.append(obv)

            elif indicator["name"] == "crossing":
                crossing = hydrate_indicator_crossing(indicator["parameters"])
                if crossing is not None:
                    indicators_builded.append(crossing)
        
        strategy[currency] = Basic(indicators_builded)
    return strategy