from algolib import get_data
from indicators.crossing import Crossing
from indicators.rsi import RSI
from exchanges.dummy import Dummy
from strategies.basic import Basic
from trade_bot import TradeBot

token = "SOL"
data = get_data(f"{token}-USD", "2013-01-01")

# Obtener los últimos 20 registros
last_records = data.iloc[-250:]

exchange = Dummy()

rsi_indicator = RSI(65, 55, 14)
crossing_indicator = Crossing(-0.01, 0, 20, 60)

strategy = Basic(indicators=[rsi_indicator, crossing_indicator])

strategy.train(last_records)

trade_bot = TradeBot(strategy, exchange, token)

index = 0
while index < len(last_records):
    current_record = last_records.iloc[index:index+1]
    trade_bot.run_strategy(current_record)
    index += 1
