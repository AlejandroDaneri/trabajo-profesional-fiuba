from lib.actions import Action
from lib.trade import Trade
from lib.exchanges.exchange import Exchange

class Dummy(Exchange):
    def __init__(self, initial_balance):
        super().__init__(initial_balance)
        self.trades = []

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

    def buy(self, symbol: str, amount: int, price: float):
        super().buy(symbol, amount, price)
        print(f"Buying {amount} units of {symbol} at {price} on Dummy Exchange.")

    def sell(self, symbol: str, amount: int, price: float):
        super().sell(symbol, amount, price)
        print(f"Selling {amount} units of {symbol} at {price} on Dummy Exchange.")

