from datetime import datetime

class Trade:
    def __init__(self, action: str, symbol: str, amount: int, price_per_unit: float):
        self.timestamp: datetime = datetime.now()
        self.action: str = action
        self.symbol: str = symbol
        self.amount: int = amount
        self.price_per_unit: float = price_per_unit
