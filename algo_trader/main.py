print("Trabajo Profesional | Algo Trading | Trader")

from lib.exchanges.dummy import Dummy
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance
from utils import hydrate_strategy

import time
import requests

def main():
    response = requests.get(url='http://localhost:8080/api/strategy')
    strategy = response.json()
    currencies = strategy["currencies"]
    indicators = strategy["indicators"]
    initial_balance = 10000

    provider = Binance()
    exchange = Dummy(initial_balance)

    strategies = hydrate_strategy(currencies, indicators)

    n_train = 250

    data = {}
    train_data = {}
    for currency in currencies:
        data[currency] = provider.get_data_from(f'{currency}USDT', '2023-12-20')
        train_data[currency] = data[currency].iloc[0:n_train]
        strategies[currency].train(train_data[currency])

    trade_bot = TradeBot(strategies, exchange)
    print("trade bot created")

    while True:
        for currency in currencies:
            data = provider.get_latest_price(f'{currency}USDT')
            print(f'Get: {currency} {data.index[0]}')
            trade = trade_bot.run_strategy(currency, data)
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
                response = requests.post(url='http://localhost:8080/api/trade', json=data)
        print("\n")
        time.sleep(60)

if __name__ == "__main__":
    main()
