from lib.actions import Action
from lib.trade import Trade
from lib.exchanges.exchange import Exchange

class Dummy(Exchange):
    def __init__(self, initial_balance=10000):
        super().__init__(initial_balance)
        self.trades = []

    def convert_all_to_usdt(ok):
        pass
    
    def buy(self, symbol: str, price: int, timestamp: float) -> Trade:
        print(f"[Exchange | Dummy] Buying {symbol}, price {price}")
        return super().buy(symbol, price, timestamp)

    def sell(self, trade: Trade, price: int, timestamp: float) -> Trade:
        print(f"[Exchange | Dummy] Selling {trade.symbol}, price {price}")
        return super().sell(trade, price, timestamp)

