from lib.indicators.crossing import Crossing
from lib.indicators.rsi import RSI
from lib.exchanges.dummy import Dummy
from lib.strategies.basic import Basic
from lib.trade_bot import TradeBot
from lib.providers.binance import Binance

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
            indicators.append(Crossing(buy_threshold, sell_threshold, slow, slow))

    strategy = Basic(indicators)
    
    train_data = data.iloc[0:1000]
    simulation_data = data.iloc[1000:1100]
    
    strategy.train(train_data)

    trade_bot = TradeBot(strategy, exchange, currency)

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

if __name__ == "__main__":
    main()