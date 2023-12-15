print("Trabajo Profesional | Algo Trading | Trader")

from lib.indicators.crossing import Crossing
from lib.indicators.rsi import RSI
from lib.exchanges.dummy import Dummy
from lib.strategies.basic import Basic
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance

import time
import requests

provider = Binance()
data = provider.get_data_from('BTCUSDT', '2023-12-08')
exchange = Dummy()

rsi_indicator = RSI(65, 55, 14)
crossing_indicator = Crossing(-0.01, 0, 20, 60)

strategy = Basic(indicators=[rsi_indicator, crossing_indicator])

last_records = data.iloc[-250:]
strategy.train(last_records)

trade_bot = TradeBot(strategy, exchange, 'BTC')

while True:
    print("getting new price")
    data = provider.get_latest_price('BTCUSDT')
    print(data)
    print("adding data to strategy")
    trade = trade_bot.run_strategy(data)
    if trade is not None:
        print(trade)
        data = {
            "pair": trade.symbol,
            "price": trade.price,
            "amount": trade.amount
        }
        r = requests.post(url='http://api:8080/trade', data=data)
    print("profit: ", trade_bot.get_profit())
    print("waiting new price")
    

    time.sleep(60)
        

