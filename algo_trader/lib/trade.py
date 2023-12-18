from datetime import datetime

class Order:
    def __init__(self, price, timestamp):
        self.price: float = price
        self.timestamp: int = timestamp

class Trade:
    def __init__(self, symbol: str, amount: int, price: float, timestamp: int):
        self.symbol: str = symbol
        self.amount: int = amount

        self.buy_order = Order(price, timestamp)
    
    def sell(self, price, timestamp):
        self.sell_order = Order(price, timestamp)

    def is_closed(self) -> bool:
        return self.sell_order is not None

