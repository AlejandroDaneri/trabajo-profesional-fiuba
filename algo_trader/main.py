print("Trabajo Profesional | Algo Trading | Trader")

from lib.trade import Trade
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance as BinanceProvider
from lib.exchanges.binance import Binance as BinanceExchange
from utils import hydrate_strategy
from api_client import ApiClient
from common.notifications.telegram.telegram_notifications_service import notify_telegram_users
import time
import sentry_sdk

sentry_sdk.init(
    dsn="https://99aef705bb2355581d11e36d65ffa585@o4506996875919360.ingest.us.sentry.io/4506996882341888",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

division_by_zero = 1 / 0

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

    # if initial balance is none, we set exchange balance as initial balance
    initial_balance = strategy["initial_balance"]
    if initial_balance is None:
        api.put('api/strategy/initial_balance', json={
            "initial_balance": str(exchange.get_balance())
        })

    api.put('api/strategy/balance', json={
        "current_balance": str(exchange.get_balance())
    })

    timeframe = strategy["timeframe"]
    type = strategy["type"]

    strategy = hydrate_strategy(type, currencies, indicators)

    n_train = 200

    data = {}
    train_data = {}
    for currency in currencies:
        data[currency] = provider.get(currency, timeframe, n=n_train)
        train_data[currency] = data[currency].iloc[0:n_train]
        strategy[currency].prepare_data(train_data[currency])

    trade_bot = TradeBot(strategy, exchange)
    
    response = api.get('api/trade/current')
    if response.status_code == 200:
        current_trade = response.json()
        print(current_trade)
        if current_trade is not None:
            print("restoring opened trade")
            print(current_trade)
            amount = current_trade["amount"]
            symbol = current_trade["pair"]
            price = current_trade["orders"]["buy"]["price"]
            timestamp = current_trade["orders"]["buy"]["timestamp"]
            trade_bot.set_current_trade(Trade(
                amount,
                symbol,
                price,
                timestamp
            ))

    while True:
        for currency in currencies:
            data = provider.get(currency, timeframe, n=1)
            print(f'Get: {currency} {data.index[0]}')
            trade = trade_bot.run_strategy(currency, data)
            if trade is not None:
                # trade closed: means buy and sell executed
                if trade.buy_order.timestamp and trade.sell_order.timestamp:
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
                    response = api.post('api/trade', json=data)

                    # remove tmp current trade
                    api.delete('api/trade/current')
                
                # trade current: buy executed but not sell yet
                if trade.buy_order.timestamp and not trade.sell_order.timestamp:
                    data = {
                        "pair": trade.symbol,
                        "amount": str(trade.amount),
                        "buy": {
                            "price": str(trade.buy_order.price),
                            "timestamp": int(trade.buy_order.timestamp)
                        }
                    }
                    response = api.post('api/trade/current', json=data)

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
