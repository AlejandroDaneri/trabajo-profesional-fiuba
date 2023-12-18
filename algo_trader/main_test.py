from lib.indicators.crossing import Crossing
from lib.indicators.rsi import RSI
from lib.exchanges.dummy import Dummy
from lib.strategies.basic import Basic
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance

import time
import requests

provider = Binance()
data = provider.get_data_from('SOLUSDT', '2023-12-08')
exchange = Dummy()

rsi_indicator = RSI(65, 55, 14)
crossing_indicator = Crossing(-0.01, 0, 20, 60)

print(len(data))
train_data = data.iloc[0:1000]
simulation_data = data.iloc[1000:1100]
strategy = Basic(indicators=[rsi_indicator, crossing_indicator])
strategy.train(train_data)

trade_bot = TradeBot(strategy, exchange, 'SOL')

response = requests.delete(url='http://algo_api:8080/api/trade')

for index in range(len(simulation_data)):
    print(index)
    row = simulation_data.iloc[[index]]
    trade = trade_bot.run_strategy(row)
    if trade is not None:
        data = {
            "pair": trade.symbol,
            "amount": str(trade.amount),
            "buy": {
                "price": str(trade.buy_order.price),
                "timestamp": int(trade.buy_order.timestamp)
            },
            "sell": {
                "price": str(trade.sell_order.price),
                "timestamp": int(trade.sell_order.timestamp)
            }
        }
        print(data)
        response = requests.post(url='http://algo_api:8080/api/trade', json=data)
