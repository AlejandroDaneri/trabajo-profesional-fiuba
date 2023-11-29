from typing import Dict

from algo_lib.actions import Action

class Exchange:
    def __init__(self, initial_balance: float = 10000.0):
        self.balance = initial_balance
        self.portfolio = {}  # Un diccionario para almacenar las tenencias de activos

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
        cost = amount * price_per_unit

        if cost > self.balance:
            raise ValueError("Insufficient funds to execute the buy order.")

        if symbol in self.portfolio:
            self.portfolio[symbol] += amount
        else:
            self.portfolio[symbol] = amount

        self.balance -= cost

    def sell(self, symbol: str, amount: int, price_per_unit: float):
        if symbol not in self.portfolio or self.portfolio[symbol] < amount:
            raise ValueError("Not enough shares to execute the sell order.")

        revenue = amount * price_per_unit
        self.portfolio[symbol] -= amount
        self.balance += revenue

    def get_portfolio(self) -> Dict[str, int]:
        return self.portfolio.copy()

    def get_balance(self) -> float:
        return self.balance

