from lib.trade_bot import TradeBot
from lib.exchanges.dummy import Dummy as DummyExchange
from lib.providers.binance import Binance as BinanceProvider
from utils import hydrate_strategy
from api_client import ApiClient

api = ApiClient()

def main():
    api.delete('trade')

    response = api.get('strategy/running')
    strategy = response.json()
    print(strategy)

    id = strategy["id"]
    type = strategy["type"]
    indicators = strategy["indicators"]
    currencies = strategy["currencies"]
    timeframe = strategy["timeframe"]

    provider = BinanceProvider()
    exchange = DummyExchange()

    exchange.convert_all_to_usdt()
    print("Balance: ", exchange.get_balance())

    api.put(f'strategy/{id}/initial_balance', json={
        "initial_balance": str(exchange.get_balance())
    })

    api.put(f'strategy/{id}/balance', json={
        "current_balance": str(exchange.get_balance())
    })

    strategy = hydrate_strategy(type, currencies, indicators, timeframe)
    
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
                    response = api.post('trade', json=data)

                    current_balance = trade_bot.get_balance()
                    api.put(f'strategy/{id}/balance', json={
                        "current_balance": str(current_balance)
                    })

        print("\n")
    
    exchange.convert_all_to_usdt()
    print("Balance: ", exchange.get_balance())

if __name__ == "__main__":
    main()