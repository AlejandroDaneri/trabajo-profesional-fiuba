print("Trabajo Profesional | Algo Trading | Trader")

from algo_lib.algolib import get_data
from algo_lib.indicators.crossing import Crossing
from algo_lib.indicators.rsi import RSI
from algo_lib.exchanges.dummy import Dummy
from algo_lib.strategies.basic import Basic
from algo_lib.trade_bot import TradeBot

import websocket
import json
import time

def main():
    token = "SOL"
    data = get_data(f"{token}-USD", "2022-01-01", "Binance")
    
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

    print("Final profit: ",trade_bot.get_profit())

    if __name__ == "__main__":
        url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
        ws = websocket.WebSocket()
        ws.connect(url)
        while True:
            message = ws.recv()
            data = json.loads(message)
            print(data['s'])
            print(data['k']['c'])
            time.sleep(60)

main()