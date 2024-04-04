from lib.actions import Action
from lib.trade import Trade
from lib.exchanges.exchange import Exchange

class Dummy(Exchange):
    def __init__(self, initial_balance=10000):
        super().__init__(initial_balance)
        self.trades = []

    def convert_all_to_usdt(ok):
        pass
    
    def place_order(self, trade: Trade, action: Action):
        symbol = trade.symbol
        amount = trade.amount

        if action == Action.BUY:
            price = trade.buy_order.price
            self.buy(symbol, amount, price)
            self.trades.append(trade)
            self.total = amount * price
            print(f"Actual portfolio: {self.portfolio}")
            print(f"Actual USDT balance: {self.balance}")
            print(f"Actual total: {self.total}")
            print(f"----------------")
        elif action == Action.SELL:
            price = trade.sell_order.price
            self.sell(symbol, amount, price)
            self.total = amount*price

            print(f"Actual portfolio: {self.portfolio}")
            print(f"Actual USDT balance: {self.balance}")
            print(f"Actual total: {self.total}")

            print(f"----------------")
        else:
            raise ValueError(
                f"Invalid action: {action}. Only 'buy' and 'sell' actions are supported."
            )

    def buy(self, symbol: str, price: int, timestamp: float) -> Trade:
        print(f"[Exchange | Dummy] Buying {symbol}, price {price}")
        return super().buy(symbol, price, timestamp)

    def sell(self, trade: Trade, price: int, timestamp: float) -> Trade:
        print(f"[Exchange | Dummy] Selling {trade.symbol}, price {price}")
        return super().sell(trade, price, timestamp)

