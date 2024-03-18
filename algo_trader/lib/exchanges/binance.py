from lib.trade import Trade
from lib.actions import Action
from lib.exchanges.exchange import Exchange

from binance.enums import *
from binance.spot import Spot as Client

class Binance(Exchange):
    def __init__(self, initial_balance):
        super().__init__(initial_balance)

        api_key = "rg4ZZURyk0DxHbPG08lKi7mVlBUTcmmWvOt7e1kDJpNNG6nozZaPS491WNbiJs3f"
        secret_key = "SnuHSKxk8wXFXh3PDG37rahOo9v7Jyg26QPm9RBSb0wT1nci29s5wkLBBGRH7V5J"

        self.client = Client(
            api_key,
            secret_key,
            base_url='https://testnet.binance.vision'
        )

        self.trades = []

    def place_order(self, trade: Trade, action: Action):
        print("placing order")
        print(trade)

        symbol = trade.symbol
        quantity = trade.amount

        if action == Action.BUY:
            price = trade.buy_order.price
            self.buy(symbol, quantity, price)
            self.trades.append(trade)
            self.total = quantity * price
        else:
            price = trade.sell_order.price
            self.sell(symbol, quantity, price)
            self.total = quantity * price

    def buy(self, symbol: str, quantity: int, price: float):
        super().buy(symbol, quantity, price)
        print(f"Buying {quantity} units of {symbol} at {price} on Dummy Exchange.")
        try:
            return
            # order = self.client.new_order(
            #    symbol=symbol,
            #    side=SIDE_BUY,
            #    type=ORDER_TYPE_MARKET,
            #    quantity=quantity
            # )
            # print(order)
        except Exception as e:
            print(f"Ocurrió un error al crear la orden: {e}")

    def sell(self, symbol: str, quantity: int, price: float):
        super().sell(symbol, quantity, price)
        print(f"Selling {quantity} units of {symbol} at {price} on Dummy Exchange.")
        try:
            return
            # order = self.client.new_order(
            #    symbol=symbol,
            #    side=SIDE_SELL,
            #    type=ORDER_TYPE_MARKET,
            #    quantity=quantity
            # )
            # print(order)
        except Exception as e:
            print(f"Ocurrió un error al crear la orden: {e}")

