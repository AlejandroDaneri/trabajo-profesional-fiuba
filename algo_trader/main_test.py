from lib.indicators.crossing import Crossing
from lib.indicators.rsi import RSI
from lib.exchanges.dummy import Dummy
from lib.strategies.basic import Basic
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance

import requests

def main():
    requests.delete(url='http://localhost:8080/api/trade')

    response = requests.get(url='http://localhost:8080/api/strategy')
    strategy = response.json()
    indicators = strategy["indicators"]
    currencies = strategy["currencies"]

    provider = Binance()
    exchange = Dummy()

    strategies = {}
    for currency in currencies:
        indicators_builded = []

        for indicator in indicators:

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
                indicators_builded.append(RSI(buy_threshold, sell_threshold, rounds))

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
                indicators_builded.append(Crossing(buy_threshold, sell_threshold, fast, slow))
        
        strategies[currency] = Basic(indicators_builded)
    
    trade_bot = TradeBot(strategies, exchange)

    data = {}
    train_data = {}
    simulation_data = {}
    
    n_train = 100
    n_simulate = 1200

    for currency in currencies:
        data[currency] = provider.get_data_from(f'{currency}USDT', '2023-11-01')
        train_data[currency] = data[currency].iloc[0:n_train]
        simulation_data[currency] = data[currency].iloc[n_train:(n_train + n_simulate)]
        strategies[currency].train(train_data[currency])

    for index in range(n_simulate):
        print(index)
        for currency in currencies:
            print(currency)
            row = simulation_data[currency].iloc[[index]]
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
                print(data)
                response = requests.post(url='http://localhost:8080/api/trade', json=data)

if __name__ == "__main__":
    main()