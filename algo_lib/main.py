from algolib import get_data
from indicators.crossing import Crossing
from indicators.rsi import RSI
from exchanges.dummy import Dummy
from strategies.basic import Basic
from trade_bot import TradeBot

data = get_data("BTC-USD", "2015-01-01")
historical_data_without_last = data.iloc[:-1]

last_record = data.iloc[-1:]
exchange = Dummy()

rsi_indicator = RSI(65, 55, 14)
crossing_indicator = Crossing(-0.01, 0, 20, 60)

strategy = Basic(indicators=[rsi_indicator, crossing_indicator])
strategy.train(historical_data_without_last)

trade_bot = TradeBot(strategy, exchange, "BTC")

new_record = data.iloc[-1:]

trade_bot.run_strategy(new_record)
