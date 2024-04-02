from lib.indicators import *
from lib.strategies.RLstrategy import RL
from lib.strategies.basic import Basic

def hydrate_strategy(type, currencies, indicators):
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

        if type == "basic":
            strategy[currency] = Basic(indicators_builded)
        elif type == "rl":
            strategy[currency] = RL(indicators_builded)

    return strategy