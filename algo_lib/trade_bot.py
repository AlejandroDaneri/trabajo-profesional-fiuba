from typing import List
from actions import Action
from exchanges.exchange import Exchange
from strategies.strategy import Strategy

from trade import Trade 

class TradeBot:
    def __init__(self, strategy: Strategy, exchange: Exchange, symbol:str):
        self.strategy = strategy
        self.exchange = exchange
        self.symbol = symbol
        self.trades = []

    def execute_trade(self, action: Action, symbol, amount):
        if action != Action.HOLD:
            trade = Trade(action, symbol, amount, 100.0) ## TODO: change this
            try:
                self.exchange.place_order(trade)
                self.trades.append(trade)
            except Exception as e:
                print(f"Error executing trade: {e}")

    def run_strategy(self, new_record):
        action = self.strategy.predict(new_record)

        amount = 10 ##TODO: fix this

        self.execute_trade(action, self.symbol, amount)

    def get_trades(self):
        return self.trades

