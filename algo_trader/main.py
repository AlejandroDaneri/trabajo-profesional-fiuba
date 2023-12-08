print("Trabajo Profesional | Algo Trading | Trader")

from algo_lib.indicators.crossing import Crossing
from algo_lib.indicators.rsi import RSI
from algo_lib.exchanges.dummy import Dummy
from algo_lib.strategies.basic import Basic
from algo_lib.trade_bot import TradeBot
from algo_lib.providers.binance import Binance

import websocket
import json
import time
import datetime

def main():
    provider = Binance()
    data = provider.get_from('BTCUSDT', '2023-12-08')
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
        print("waiting new price")
        time.sleep(60)
        print("getting new price")
        data = provider.get_latest_price('BTCUSDT')
        print(data)
        print("adding data to strategy")
        trade_bot.run_strategy(data)
        

main()