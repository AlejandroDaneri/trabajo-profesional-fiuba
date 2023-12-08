print("Trabajo Profesional | Algo Trading | Trader")

from lib.indicators.crossing import Crossing
from lib.indicators.rsi import RSI
from lib.exchanges.dummy import Dummy
from lib.strategies.basic import Basic
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance

import websocket
import json
import time
import datetime

provider = Binance()
data = provider.get_data_from('BTCUSDT', '2023-12-08')
exchange = Dummy()

rsi_indicator = RSI(65, 55, 14)
crossing_indicator = Crossing(-0.01, 0, 20, 60)

strategy = Basic(indicators=[rsi_indicator, crossing_indicator])

last_records = data.iloc[-250:]
strategy.train(last_records)

trade_bot = TradeBot(strategy, exchange, 'BTC')

#index = 0
#while index < len(last_records):
#    current_record = last_records.iloc[index:index+1]
#    trade_bot.run_strategy(current_record)
#    index += 1

#print("Final profit: ", trade_bot.get_profit())

#return

while True:
    print("getting new price")
    data = provider.get_latest_price('BTCUSDT')
    print(data)
    print("adding data to strategy")
    trade_bot.run_strategy(data)
    print("profit: ", trade_bot.get_profit())
    print("waiting new price")
    time.sleep(60)
        

