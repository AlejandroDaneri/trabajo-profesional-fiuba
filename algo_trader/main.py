print("Trabajo Profesional | Algo Trading | Trader")

from lib.indicators.crossing import Crossing
from lib.indicators.rsi import RSI
from lib.exchanges.dummy import Dummy
from lib.strategies.basic import Basic
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance

import time
import requests

def main():
    response = requests.get(url='http://algo_api:8080/api/strategy')
    strategy = response.json()

    # for now only one currency at the same time
    currency = strategy["currencies"][0]

    provider = Binance()
    data = provider.get_data_from(f'{currency}USDT', '2023-12-08')
    exchange = Dummy()

    indicators = []
    for indicator in strategy["indicators"]:

        if indicator["name"] == "rsi":
            parameters = indicator["parameters"]
            if parameters is None:
                print("indicator rsi not have parameters")
                continue
            buy_threshold = parameters["buy_threshold"]
            sell_threshold = parameters["sell_threshold"]
            rounds = parameters["rounds"]
            if buy_threshold is None or sell_threshold is None or rounds is None:
                print("indicator rsi not have all the parameters")
                continue
            indicators.append(RSI(buy_threshold, sell_threshold, rounds))

        elif indicator["name"] == "crossing":
            parameters = indicator["parameters"]
            if parameters is None:
                print("indicator crossing not have parameters")
                continue
            buy_threshold = parameters["buy_threshold"]
            sell_threshold = parameters["sell_threshold"]
            fast = parameters["fast"]
            slow = parameters["slow"]
            if buy_threshold is None or sell_threshold is None or fast is None or slow is None:
                print("indicator crossing not have all the parameters")
                continue
            indicators.append(Crossing(buy_threshold, sell_threshold, fast, slow))

    strategy = Basic(indicators)

    last_records = data.iloc[-250:]
    strategy.train(last_records)

    trade_bot = TradeBot(strategy, exchange, currency)

    while True:
        print("getting new price")
        data = provider.get_latest_price(f'{currency}USDT')
        print(data)
        print("adding data to strategy")
        trade = trade_bot.run_strategy(data)
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
        time.sleep(60)

if __name__ == "__main__":
    main()
