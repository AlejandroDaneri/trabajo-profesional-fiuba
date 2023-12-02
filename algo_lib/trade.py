from datetime import datetime

from algo_lib.exchanges.exchange import Exchange

class Trade:
    def __init__(self, action: str, symbol: str, amount: int, exchange: Exchange):
        self.timestamp: datetime = datetime.now()
        self.action: str = action
        self.symbol: str = symbol
        self.amount: int = amount
        self.exchange: Exchange = exchange


