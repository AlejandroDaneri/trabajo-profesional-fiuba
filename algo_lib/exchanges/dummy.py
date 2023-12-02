from algo_lib.actions import Action
from algo_lib.exchanges.exchange import Exchange

class Dummy(Exchange):
    def __init__(self):
        super().__init__(self)

    def place_order(self, trade):
        action = trade.action.lower()
        symbol = trade.symbol
        amount = trade.amount
        price_per_unit = trade.price_per_unit

        if action == Action.BUY:
            self.buy(symbol, amount, price_per_unit)
        elif action == Action.SELL:
            self.sell(symbol, amount, price_per_unit)
        else:
            raise ValueError(f"Invalid action: {action}. Only 'buy' and 'sell' actions are supported.")

    def buy(self, symbol: str, amount: int, price_per_unit: float):
        super().buy()
        print(f"Buying {amount} units of {symbol} on Dummy Exchange.")

    def sell(self, symbol: str, amount: int, price_per_unit: float):
        super().sell()
        print(f"Selling {amount} units of {symbol} on Dummy Exchange.")


