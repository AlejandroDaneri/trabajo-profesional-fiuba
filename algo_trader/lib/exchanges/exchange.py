from abc import abstractmethod
from typing import Dict
from lib.actions import Action
from lib.trade import Trade, Order

class Exchange:
    def __init__(self, initial_balance: float = 10000.0):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.portfolio = {}
        self.total = self.balance

    def buy(self, symbol: str, price: int, timestamp: float) -> Trade:
        amount = self.total / price

        if symbol in self.portfolio:
            self.portfolio[symbol] += amount
        else:
            self.portfolio[symbol] = amount

        self.total = amount * price

        return Trade(
            symbol,
            amount,
            price,
            timestamp
        )

    def sell(self, trade: Trade, price: int, timestamp: int) -> Trade:
        symbol = trade.symbol
        amount = trade.amount

        self.balance = self.portfolio[symbol] * price
        self.portfolio[symbol] = 0

        trade.sell_order = Order(price, timestamp)

        self.total = amount * price

        return trade

    def get_portfolio(self) -> Dict[str, int]:
        return self.portfolio.copy()

    def get_balance(self) -> float:
        return self.total
    
    def get_profit_and_loss(self):
        return self.total - self.initial_balance 
