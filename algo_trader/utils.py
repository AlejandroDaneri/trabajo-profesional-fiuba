from lib.indicators.rsi import RSI
from lib.indicators.macd import MACD
from lib.indicators.bbands import BBANDS
from lib.indicators.dmi import DMI
from lib.indicators.ema import EMA
from lib.indicators.sma import SMA
from lib.indicators.crossingEma import CrossingEMA
from lib.indicators.crossingSma import CrossingSMA
from lib.indicators.threeEma import ThreeEMA
from lib.indicators.threeSma import ThreeSMA
from lib.indicators.obv import OBV
from lib.indicators.nvi import NVI
from lib.indicators.pvi import PVI
from lib.indicators.mfi import MFI
from lib.indicators.stochastic import Stochastic
from lib.indicators.koncorde import KONCORDE
from lib.indicators.sar import SAR
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
    di_rounds = parameters["di_rounds"]
    adx_rounds = parameters["adx_rounds"]
    adx_threshold = parameters["adx_threshold"]
    if di_rounds is None or adx_rounds is None or adx_threshold is None:
        print("indicator dmi not have all the parameters")
        return None
    return DMI(di_rounds, adx_rounds, adx_threshold)

def hydrate_indicator_ema(parameters):
    if parameters is None:
        print("indicator ema not have parameters")
        return None
    rounds = parameters["rounds"]
    if rounds is None:
        print("indicator ema not have all the parameters")
        return None
    return EMA(rounds)

def hydrate_indicator_crossing_ema(parameters):
    if parameters is None:
        print("indicator crossing ema not have parameters")
        return None
    fast_rounds = parameters["fast_rounds"]
    slow_rounds = parameters["slow_rounds"]
    if fast_rounds is None or slow_rounds is None:
        print("indicator crossing ema not have all the parameters")
        return None
    return CrossingEMA(fast_rounds, slow_rounds)

def hydrate_indicator_three_ema(parameters):
    if parameters is None:
        print("indicator three ema not have parameters")
        return None
    fast_rounds = parameters["fast_rounds"]
    slow_rounds = parameters["slow_rounds"]
    support_rounds = parameters["support_rounds"]
    if fast_rounds is None or slow_rounds is None or support_rounds is None:
        print("indicator three ema not have all the parameters")
        return None
    return ThreeEMA(fast_rounds, slow_rounds, support_rounds)

def hydrate_indicator_sma(parameters):
    if parameters is None:
        print("indicator sma not have parameters")
        return None
    rounds = parameters["rounds"]
    if rounds is None:
        print("indicator sma not have all the parameters")
        return None
    return SMA(rounds)

def hydrate_indicator_crossing_sma(parameters):
    if parameters is None:
        print("indicator crossing sma not have parameters")
        return None
    fast_rounds = parameters["fast_rounds"]
    slow_rounds = parameters["slow_rounds"]
    if fast_rounds is None or slow_rounds is None:
        print("indicator crossing sma not have all the parameters")
        return None
    return CrossingSMA(fast_rounds, slow_rounds)

def hydrate_indicator_three_sma(parameters):
    if parameters is None:
        print("indicator three sma not have parameters")
        return None
    fast_rounds = parameters["fast_rounds"]
    slow_rounds = parameters["slow_rounds"]
    support_rounds = parameters["support_rounds"]
    if fast_rounds is None or slow_rounds is None or support_rounds is None:
        print("indicator three sma not have all the parameters")
        return None
    return ThreeSMA(fast_rounds, slow_rounds, support_rounds)

def hydrate_indicator_obv(parameters):
    if parameters is None:
        print("indicator obv not have parameters")
        return None
    rounds = parameters["rounds"]
    if rounds is None:
        print("indicator obv not have all the parameters")
        return None
    return OBV(rounds)

def hydrate_indicator_nvi(parameters):
    if parameters is None:
        print("indicator nvi not have parameters")
        return None
    rounds = parameters["rounds"]
    if rounds is None:
        print("indicator nvi not have all the parameters")
        return None
    return NVI(rounds)

def hydrate_indicator_pvi(parameters):
    if parameters is None:
        print("indicator pvi not have parameters")
        return None
    rounds = parameters["rounds"]
    if rounds is None:
        print("indicator pvi not have all the parameters")
        return None
    return PVI(rounds)

def hydrate_indicator_mfi(parameters):
    if parameters is None:
        print("indicator mfi not have parameters")
        return None
    buy_threshold = parameters["buy_threshold"]
    sell_threshold = parameters["sell_threshold"]
    rounds = parameters["rounds"]
    if buy_threshold is None or sell_threshold is None or rounds is None:
        print("indicator mfi not have all the parameters")
        return None
    return MFI(buy_threshold, sell_threshold, rounds)

def hydrate_indicator_stochastic(parameters):
    if parameters is None:
        print("indicator stochastic not have parameters")
        return None
    buy_threshold = parameters["buy_threshold"]
    sell_threshold = parameters["sell_threshold"]
    rounds = parameters["rounds"]
    if buy_threshold is None or sell_threshold is None or rounds is None:
        print("indicator stochastic not have all the parameters")
        return None
    return Stochastic(buy_threshold, sell_threshold, rounds)

def hydrate_indicator_koncorde(parameters):
    if parameters is None:
        print("indicator koncorde not have parameters")
        return None
    rounds = parameters["rounds"]
    rsi_mfi_length = parameters["rsi_mfi_length"]
    bbands_length = parameters["bbands_length"]
    bbands_factor = parameters["bbands_factor"]
    stoch_length = parameters["stoch_length"]
    if rounds is None or rsi_mfi_length is None or bbands_length is None or bbands_factor is None or stoch_length is None:
        print("indicator koncorde not have all the parameters")
        return None
    return KONCORDE(rounds, rsi_mfi_length, bbands_length, bbands_factor, stoch_length)

def hydrate_indicator_sar(parameters):
    if parameters is None:
        print("indicator sar not have parameters")
        return None
    initial_af = parameters["initial_af"]
    max_af = parameters["max_af"]
    af_increment = parameters["af_increment"]
    if initial_af is None or max_af is None or af_increment is None:
        print("indicator sar not have all the parameters")
        return None
    return SAR(initial_af, max_af, af_increment)

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

            elif indicator["name"] == "crossing_ema":
                crossing_ema = hydrate_indicator_crossing_ema(indicator["parameters"])
                if crossing_ema is not None:
                    indicators_builded.append(crossing_ema)

            elif indicator["name"] == "crossing_sma":
                crossing_sma = hydrate_indicator_crossing_sma(indicator["parameters"])
                if crossing_sma is not None:
                    indicators_builded.append(crossing_sma)

            elif indicator["name"] == "three_ema":
                three_ema = hydrate_indicator_three_ema(indicator["parameters"])
                if three_ema is not None:
                    indicators_builded.append(three_ema)

            elif indicator["name"] == "three_sma":
                three_sma = hydrate_indicator_three_sma(indicator["parameters"])
                if three_sma is not None:
                    indicators_builded.append(three_sma)

            elif indicator["name"] == "nvi":
                nvi = hydrate_indicator_nvi(indicator["parameters"])
                if nvi is not None:
                    indicators_builded.append(nvi)

            elif indicator["name"] == "pvi":
                pvi = hydrate_indicator_pvi(indicator["parameters"])
                if pvi is not None:
                    indicators_builded.append(pvi)

            elif indicator["name"] == "mfi":
                mfi = hydrate_indicator_mfi(indicator["parameters"])
                if mfi is not None:
                    indicators_builded.append(mfi)

            elif indicator["name"] == "stochastic":
                stochastic = hydrate_indicator_stochastic(indicator["parameters"])
                if stochastic is not None:
                    indicators_builded.append(stochastic)

            elif indicator["name"] == "koncorde":
                koncorde = hydrate_indicator_koncorde(indicator["parameters"])
                if koncorde is not None:
                    indicators_builded.append(koncorde)

            elif indicator["name"] == "sar":
                sar = hydrate_indicator_sar(indicator["parameters"])
                if sar is not None:
                    indicators_builded.append(sar)
        
        strategy[currency] = Basic(indicators_builded)
    return strategy