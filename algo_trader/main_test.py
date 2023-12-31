from lib.exchanges.dummy import Dummy
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance
from utils import hydrate_strategy

import requests

def main():
    requests.delete(url='http://localhost:8080/api/trade')

    response = requests.get(url='http://localhost:8080/api/strategy')
    strategy = response.json()
    print(strategy)
    indicators = strategy["indicators"]
    currencies = strategy["currencies"]
    initial_balance = 10000
    timeframe = strategy["timeframe"]

    provider = Binance()
    exchange = Dummy(initial_balance)

    strategy = hydrate_strategy(currencies, indicators)
    
    data = {}
    train_data = {}
    simulation_data = {}
    
    n_train = 200
    n_simulate = 6000
    n_total = n_train + n_simulate

    for currency in currencies:
        data[currency] = provider.get_latest_n(f'{currency}USDT', timeframe, n_total)
        train_data[currency] = data[currency].iloc[0:n_train]
        simulation_data[currency] = data[currency].iloc[n_train:n_total]
        strategy[currency].train(train_data[currency])

    trade_bot = TradeBot(strategy, exchange)

    for index in range(n_simulate):
        
        for currency in currencies:
            row = simulation_data[currency].iloc[[index]]
            print(f'Simulating: {currency} {row.index[0]}')
            trade = trade_bot.run_strategy(currency, row)
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
                response = requests.post(url='http://localhost:8080/api/trade', json=data)
        
        print("\n")
    
    print("Balance: {}".format(trade_bot.get_balance()))

if __name__ == "__main__":
    main()