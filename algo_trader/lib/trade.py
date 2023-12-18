from datetime import datetime

class Trade:
    def __init__(self, action: str, symbol: str, amount: int, price: float):
        self.timestamp: datetime = datetime.now()
        self.action: str = action
        self.symbol: str = symbol
        self.amount: int = amount
        self.price: float = price
