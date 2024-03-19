print("Trabajo Profesional | Algo Trading | Trader")

from lib.trade_bot import TradeBot
from lib.providers.binance import Binance as BinanceProvider
from lib.exchanges.binance import Binance as BinanceExchange
from utils import hydrate_strategy
from api_client import ApiClient
from common.notifications.telegram.telegram_notifications_service import notify_telegram_users

import time

api = ApiClient()

def main():
    response = api.get('api/strategy/running')
    strategy = response.json()
    print(strategy)
    indicators = strategy["indicators"]
    currencies = strategy["currencies"]

    provider = BinanceProvider()
    exchange = BinanceExchange()

    exchange.convert_all_to_usdt()
    print(f"Initial Balance: {exchange.get_balance()}")

    api.put('api/strategy/initial_balance', json={
        "initial_balance": str(exchange.get_balance())
    })

    api.put('api/strategy/balance', json={
        "current_balance": str(exchange.get_balance())
    })

    timeframe = strategy["timeframe"]

    strategy = hydrate_strategy(currencies, indicators)

    n_train = 200

    data = {}
    train_data = {}
    for currency in currencies:
        data[currency] = provider.get(currency, timeframe, n=n_train)
        train_data[currency] = data[currency].iloc[0:n_train]
        strategy[currency].train(train_data[currency])

    trade_bot = TradeBot(strategy, exchange)
    print("trade bot created")

    while True:
        for currency in currencies:
            data = provider.get(currency, timeframe, n=1)
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
                response = api.post('api/trade', json=data)

                trade_details_message = (
                "Trade Details:\n"
                "Pair: {}\n"
                "Amount: {}\n"
                "Buy Order:\n"
                "  Price: {}\n"
                "  Timestamp: {}\n"
                "Sell Order:\n"
                "  Price: {}\n"
                "  Timestamp: {}"
                ).format(
                    data['pair'],
                    data['amount'],
                    data['buy']['price'],
                    data['buy']['timestamp'],
                    data['sell']['price'],
                    data['sell']['timestamp']
                )

                notify_telegram_users(trade_details_message)

                current_balance = trade_bot.get_balance()
                print(f"Current balance: {current_balance}")

                api.put('api/strategy/balance', json={
                    "current_balance": str(current_balance)
                })
        print("\n")
        time.sleep(60)

if __name__ == "__main__":
    main()
