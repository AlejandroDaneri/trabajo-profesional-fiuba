from lib.trade import Trade
from lib.actions import Action
from lib.exchanges.exchange import Exchange

from binance.enums import *
from binance.spot import Spot as Client
import numpy

class Binance(Exchange):
    def __init__(self):
        api_key = "rg4ZZURyk0DxHbPG08lKi7mVlBUTcmmWvOt7e1kDJpNNG6nozZaPS491WNbiJs3f"
        secret_key = "SnuHSKxk8wXFXh3PDG37rahOo9v7Jyg26QPm9RBSb0wT1nci29s5wkLBBGRH7V5J"

        self.client = Client(
            api_key,
            secret_key,
            base_url='https://testnet.binance.vision'
        )

        super().__init__(self.get_balance())

        self.trades = []

    def place_order(self, trade: Trade, action: Action):
        symbol = trade.symbol
        quantity = trade.amount
        price = self.get_price(symbol)
        if action == Action.BUY:
            self.buy(symbol, None, None)
            self.trades.append(trade)
            self.total = quantity * price
        else:
            self.sell(symbol, None, None)
            self.total = quantity * price

    def get_balance_symbol(self, symbol: str) -> float:
        balances = self.client.account()['balances']
        for index, value in enumerate(balances):
            if value['asset'] == symbol:
                return float(value['free'])

    def get_balance(self) -> float:
        return self.get_balance_symbol('USDT')

    def get_price(self, symbol) -> float:
        return float(self.client.ticker_price(symbol=f"{symbol}USDT")["price"])
    
    def execute_buy_order(self, symbol):
        try:
            remanent = 100
            while(self.get_balance() > remanent):
                print(f"trying to BUY: {self.get_balance()}")

                order = self.client.new_order(
                    symbol = f"{symbol}USDT",
                    side = SIDE_BUY,
                    type = ORDER_TYPE_MARKET,
                    quoteOrderQty = self.get_balance()
                )
        except Exception as e:
            print(f"Ocurrió un error al crear la orden: {e}")
    
    def execute_sell_order(self, symbol):
        try:
            while(self.get_balance_symbol(symbol) > 0):
                print(f"trying to BUY symbol: {symbol}, amount: {self.get_balance_symbol(symbol)}")

                order = self.client.new_order(
                    symbol = f"{symbol}USDT",
                    side = SIDE_SELL,
                    type = ORDER_TYPE_MARKET,
                    quantity = float(round(self.get_balance_symbol(symbol), 5))
                )
        except Exception as e:
            print(f"Ocurrió un error al crear la orden: {e}")
        
    
    def execute_order(self, symbol: str, target: float, side):
        try:
            filled = float(0)

            while(filled < target):
                quantity = float(round(float(target) - filled, 5))

                if side is SIDE_BUY:
                    print(f"trying to BUY: {quantity}")
                
                if side is SIDE_SELL:
                    print(f"trying to SELL: {quantity}")

                order = self.client.new_order(
                    symbol = f"{symbol}USDT",
                    side = side,
                    type = ORDER_TYPE_MARKET,
                    quantity = quantity,
                )

                filled = filled + float(order['executedQty'])
        except Exception as e:
            print(f"Ocurrió un error al crear la orden: {e}")

    def buy(self, symbol: str, quantity: float, price: float):
        print(f"[Exchange | Binance] Buying quantity: {symbol}")
        self.execute_buy_order(symbol)
        self.portfolio[symbol] = self.get_balance_symbol(symbol)
        #super().buy(symbol, quantity, price)

    def sell(self, symbol: str, quantity: int, price: float):
        print(f"[Exchange | Binance] Selling quantity: {symbol}")
        self.execute_sell_order(symbol)
        self.portfolio[symbol] = self.get_balance_symbol(symbol)
        #super().sell(symbol, quantity, price)

    def convert_all_to_usdt(self):
        print("[Exchange | Binance] converting all to USDT")
        print(f"[Exchange | Binance] balance USDT: {self.get_balance()}")
        balances = self.client.account()['balances']
        for index, value in enumerate(balances):
            symbol = value['asset']
            if symbol not in ['BTC', 'SOL', 'ETH']:
                continue
            quantity = float(value['free'])
            if symbol != 'USDT':
                self.execute_order(symbol, quantity, SIDE_SELL)
        print("[Exchange | Binance] convertion completed")
        print(f"[Exchange | Binance] balance USDT: {self.get_balance()}")

    

