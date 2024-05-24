from lib.actions import Action
from lib.exchanges.dummy import Dummy
from lib.strategies.strategy import Strategy
from lib.trade import Trade

class TradeBot:
    def __init__(self, strategy: dict[Strategy]):
        self.strategy = strategy
        self.exchange = Dummy()
        self.trades = []
        self.stop_loss_ratio = 0.2

        self.current_trade = None

    def run_strategy(self, currency, new_record):
        action = self.strategy[currency].predict(new_record)

        timestamp = new_record["Timestamp"][0]
        price = new_record["Close"][0]

        if (self.trades): 
            # Check for stop-loss condition before executing a sell order
            if (
                self.current_trade is not None
                and self.current_trade.symbol == currency
                and price < self.current_trade.buy_order.price * (1 - self.stop_loss_ratio)
            ):
                # stop loss trigger sell
                trade = self.exchange.sell(currency, price, timestamp)
                return trade


        buy_condition = action == Action.BUY and (self.current_trade is None)
        sell_condition = action == Action.SELL and (self.current_trade is not None) and (self.current_trade.symbol == currency)

        if buy_condition:
            trade = self.exchange.buy(currency, price, timestamp)
            self.current_trade = trade
            return trade

        elif sell_condition:
            trade = self.exchange.sell(self.current_trade, price, timestamp)
            self.current_trade = None
            return trade
        else:
            return None

    def set_current_trade(self, trade: Trade):
        self.current_trade = self.exchange.buy(trade.symbol, float(trade.buy_order.price), trade.buy_order.timestamp)

    def get_trades(self):
        return self.trades
    
    def get_balance(self):
        return self.exchange.get_balance()
    
    def get_profit_and_loss(self):
        return self.exchange.get_profit_and_loss()
