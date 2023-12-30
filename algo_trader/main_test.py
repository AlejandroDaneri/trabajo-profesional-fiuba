from lib.indicators.crossing import Crossing
from lib.indicators.rsi import RSI
from lib.exchanges.dummy import Dummy
from lib.strategies.basic import Basic
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance

import requests

def hydrate_indicator_rsi(parameters):
    if parameters is None:
        print("indicator rsi not have parameters")
        return None
    buy_threshold = parameters["buy_threshold"]
    sell_threshold = parameters["sell_threshold"]
    rounds = parameters["rounds"]
    if buy_threshold is None or sell_threshold is None or rounds is None:
        print("indicator rsi not have all the parameters")
        return None
    return RSI(buy_threshold, sell_threshold, rounds)

def hydrate_indicator_crossing(parameters):
    if parameters is None:
        print("indicator crossing not have parameters")
        return None
    buy_threshold = parameters["buy_threshold"]
    sell_threshold = parameters["sell_threshold"]
    fast = parameters["fast"]
    slow = parameters["slow"]
    if buy_threshold is None or sell_threshold is None or fast is None or slow is None:
        print("indicator crossing not have all the parameters")
        return None
    return Crossing(buy_threshold, sell_threshold, fast, slow)

def hydrate_strategy(currencies, indicators):
    strategies = {}
    for currency in currencies:
        indicators_builded = []

        for indicator in indicators:
            if indicator["name"] == "rsi":
                rsi = hydrate_indicator_rsi(indicator["parameters"])
                if rsi is not None:
                    indicators_builded.append(rsi)

            elif indicator["name"] == "crossing":
                crossing = hydrate_indicator_crossing(indicator["parameters"])
                if crossing is not None:
                    indicators_builded.append(crossing)
        
        strategies[currency] = Basic(indicators_builded)
    return strategies

def main():
    requests.delete(url='http://localhost:8080/api/trade')

    response = requests.get(url='http://localhost:8080/api/strategy')
    strategy = response.json()
    indicators = strategy["indicators"]
    currencies = strategy["currencies"]
    initial_balance = 10000

    provider = Binance()
    exchange = Dummy(initial_balance)

    strategies = hydrate_strategy(currencies, indicators)
    
    trade_bot = TradeBot(strategies, exchange)

    data = {}
    train_data = {}
    simulation_data = {}
    
    n_train = 100
    n_simulate = 6000

    for currency in currencies:
        data[currency] = provider.get_data_from(f'{currency}USDT', '2023-12-25')
        train_data[currency] = data[currency].iloc[0:n_train]
        simulation_data[currency] = data[currency].iloc[n_train:(n_train + n_simulate)]
        strategies[currency].train(train_data[currency])

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