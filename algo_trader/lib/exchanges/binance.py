from lib.trade import Trade
from lib.actions import Action
from binance.enums import *
from binance.spot import Spot as Client

class Binance:
    def __init__(self):
        api_key = "rg4ZZURyk0DxHbPG08lKi7mVlBUTcmmWvOt7e1kDJpNNG6nozZaPS491WNbiJs3f"
        secret_key = "SnuHSKxk8wXFXh3PDG37rahOo9v7Jyg26QPm9RBSb0wT1nci29s5wkLBBGRH7V5J"

        self.client = Client(
            api_key,
            secret_key,
            base_url='https://testnet.binance.vision'
        )

    def place_order(self, trade: Trade, action: Action):
        print("placing order")
        print(trade)

        symbol = trade.symbol
        quantity = trade.amount

        if action == Action.BUY:
            side = SIDE_BUY
        else:
            side = SIDE_SELL

        try:
            order = self.client.new_order(
                symbol=symbol,
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )
            print(order)
        except Exception as e:
            print(f"Ocurrió un error al crear la orden: {e}")
