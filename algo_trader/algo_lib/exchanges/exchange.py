from abc import abstractmethod
from typing import Dict

from algo_lib.trade import Trade

class Exchange:
    def __init__(self, initial_balance: float = 10000.0):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.portfolio = {}
        self.total = self.balance

    @abstractmethod
    def place_order(self, trade: Trade):
        pass

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
            raise ValueError("Not enough asset to execute the sell order.")

        revenue = amount * price_per_unit
        self.portfolio[symbol] -= amount
        self.balance += revenue

    def get_portfolio(self) -> Dict[str, int]:
        return self.portfolio.copy()

    def get_balance(self) -> float:
        return self.balance
    
    def get_profit(self):
        return self.total - self.initial_balance 
