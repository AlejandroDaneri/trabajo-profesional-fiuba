from lib.trade import Trade
from lib.actions import Action
from lib.exchanges.exchange import Exchange
from lib.trade import Order

from binance.enums import *
from binance.spot import Spot as Client
import os
import time

class Binance(Exchange):
    def __init__(self):
        api_key = os.getenv('EXCHANGE_BINANCE_API_KEY')
        secret_key = os.getenv('EXCHANGE_BINANCE_API_SECRET')

        self.client = Client(
            api_key,
            secret_key,
            base_url='https://testnet.binance.vision'
        )

        super().__init__(self.get_balance_symbol('USDT'))

        self.trades = []

    def get_balance_symbol(self, symbol: str) -> float:
        balances = self.client.account()['balances']
        for index, value in enumerate(balances):
            if value['asset'] == symbol:
                return float(value['free'])

    def get_balance(self) -> float:
        total = 0
        for symbol in ['SOL', 'ETH', 'BTC']:
            total = total + (self.get_balance_symbol(symbol) * self.get_price(symbol))
        return total + self.get_balance_symbol('USDT')

    def get_price(self, symbol) -> float:
        return float(self.client.ticker_price(symbol=f"{symbol}USDT")["price"])
    
    def execute_buy_order(self, symbol):
        try:
            remanent = 100
            while(True):
                balance_usdt = self.get_balance_symbol('USDT')
                if balance_usdt > remanent:
                    break
                # fix to: "Too much request weight used; current limit is 6000 request weight per 1 MINUTE"
                time.sleep(60 / 6000)
                order = self.client.new_order(
                    symbol = f"{symbol}USDT",
                    side = SIDE_BUY,
                    type = ORDER_TYPE_MARKET,
                    quoteOrderQty = balance_usdt
                )

                print(f"[Exchange | Binance] filled: {order['executedQty']}")
        except Exception as e:
            print(f"Ocurrió un error al crear la orden: {e}")
    
    def execute_sell_order(self, symbol: str):
        try:
            while(self.get_balance_symbol(symbol) > 0):
                # fix to: "Too much request weight used; current limit is 6000 request weight per 1 MINUTE"
                time.sleep(60 / 6000)
                print(f"trying to BUY symbol: {symbol}, amount: {self.get_balance_symbol(symbol)}")

                order = self.client.new_order(
                    symbol = f"{symbol}USDT",
                    side = SIDE_SELL,
                    type = ORDER_TYPE_MARKET,
                    quantity = float(round(self.get_balance_symbol(symbol), 5))
                )

                print(f"[Exchange | Binance] filled: {order['executedQty']}")
        except Exception as e:
            print(f"Ocurrió un error al crear la orden: {e}")
        
    def buy(self, symbol: str, price: int, timestamp: float) -> Trade:
        print(f"[Exchange | Binance] Buying symbol: {symbol}")
        self.execute_buy_order(symbol)
        self.portfolio[symbol] = self.get_balance_symbol(symbol)
        print(f"[Exchange | Binance] amount: {self.get_balance_symbol(symbol)}")

        return Trade(
            symbol,
            self.get_balance_symbol(symbol),
            self.get_price(symbol),
            time.time()
        )

    def sell(self, trade: Trade, price: int, timestamp: int) -> Trade:
        print(f"[Exchange | Binance] Selling quantity: {trade.symbol}")
        self.execute_sell_order(trade.symbol)
        self.portfolio[trade.symbol] = self.get_balance_symbol(trade.symbol)
        print(f"[Exchange | Binance] amount: {self.get_balance_symbol(trade.symbol)}")

        trade.sell_order = Order(
            self.get_price(trade.symbol),
            time.time()
        )

        return trade

    def convert_all_to_usdt(self):
        print("[Exchange | Binance] converting all to USDT")
        print(f"[Exchange | Binance] balance USDT: {self.get_balance_symbol('USDT')}")
        balances = self.client.account()['balances']
        for index, value in enumerate(balances):
            symbol = value['asset']
            if symbol not in ['BTC', 'SOL', 'ETH']:
                continue
            self.execute_sell_order(symbol)
        print("[Exchange | Binance] convertion completed")
        print(f"[Exchange | Binance] balance USDT: {self.get_balance_symbol('USDT')}")

    

