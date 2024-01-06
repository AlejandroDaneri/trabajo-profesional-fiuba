from abc import abstractmethod
from typing import Dict
from lib.actions import Action
from lib.trade import Trade

class Exchange:
    def __init__(self, initial_balance: float = 10000.0):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.portfolio = {}
        self.total = self.balance

    @abstractmethod
    def place_order(self, trade: Trade, type: Action):
        pass

    def buy(self, symbol: str, amount: int, price: float):
        cost = amount * price

        if int(cost) > int(self.balance):
            raise ValueError("Insufficient funds to execute the buy order.")

        if symbol in self.portfolio:
            self.portfolio[symbol] += amount
        else:
            self.portfolio[symbol] = amount

        self.balance -= cost

    def sell(self, symbol: str, amount: int, price: float):
        if symbol not in self.portfolio or self.portfolio[symbol] < amount:
            raise ValueError("Not enough asset to execute the sell order.")

        revenue = amount * price
        self.portfolio[symbol] -= amount
        self.balance += revenue

    def get_portfolio(self) -> Dict[str, int]:
        return self.portfolio.copy()

    def get_balance(self) -> float:
        return self.balance
    
    def get_profit_and_loss(self):
        return self.total - self.initial_balance 
