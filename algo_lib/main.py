from algolib import *
from indicators import *
from indicators.rsi import RSI
from indicators.sigma import Sigma
from indicators.crossing import Crossing

data = get_data('BTC-USD', '2015-01-01')

from strategies.basic import Basic

rsi_indicator = RSI(65, 55, 14)
crossing_indicator = Crossing(-0.01, 0, 20, 60)

basic_strategy = Basic(indicators=[rsi_indicator, crossing_indicator])


historical_data_without_last = data.iloc[:-1]
basic_strategy.train(historical_data_without_last)

last_record = data.iloc[-1:]

signal = basic_strategy.predict(last_record)
print(signal)