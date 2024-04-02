from lib.trade_bot import TradeBot
from lib.exchanges.dummy import Dummy
from lib.providers.binance import Binance as BinanceProvider
from utils import hydrate_strategy
from api_client import ApiClient

api = ApiClient()

def main():
    api.delete('api/trade')

    response = api.get('api/strategy/running')
    strategy = response.json()
    print(strategy)
    indicators = strategy["indicators"]
    currencies = strategy["currencies"]
    timeframe = strategy["timeframe"]

    provider = BinanceProvider()
    exchange = Dummy()

    exchange.convert_all_to_usdt()
    print("Balance: ", exchange.get_balance())

    api.put('api/strategy/initial_balance', json={
        "initial_balance": str(exchange.get_balance())
    })

    api.put('api/strategy/balance', json={
        "current_balance": str(exchange.get_balance())
    })

    strat_type = strategy["type"]

    strategy = hydrate_strategy(strat_type,currencies, indicators)
    
    data = {}
    train_data = {}
    simulation_data = {}
    
    n_train = 200
    n_simulate = 300
    n_total = n_train + n_simulate

    for currency in currencies:
        data[currency] = provider.get(currency, timeframe, n=n_total)
        train_data[currency] = data[currency].iloc[0:n_train]
        simulation_data[currency] = data[currency].iloc[n_train:n_total]
        strategy[currency].prepare_data(train_data[currency])

    trade_bot = TradeBot(strategy, exchange)

    for index in range(n_simulate):
        for currency in currencies:
            row = simulation_data[currency].iloc[[index]]
            print(f'Simulating: {currency} {row.index[0]}')
            trade = trade_bot.run_strategy(currency, row)
            if trade is not None:
                # trade closed: means buy and sell executed
                if trade.is_closed():
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

                    response = api.post('api/trade/current', json=data)
                    
                    # update balance to strategy doc in the db
                    current_balance = trade_bot.get_balance()
                    print(f"Current balance: {current_balance}")
                    api.put('api/strategy/balance', json={
                        "current_balance": str(current_balance)
                    })
                else:
                    # trade current: buy executed but not sell yet
                    data = {
                        "pair": trade.symbol,
                        "amount": str(trade.amount),
                        "buy": {
                            "price": str(trade.buy_order.price),
                            "timestamp": int(trade.buy_order.timestamp)
                        }
                    }

        print("\n")
    
    exchange.convert_all_to_usdt()
    print("Balance: ", exchange.get_balance())

if __name__ == "__main__":
    main()