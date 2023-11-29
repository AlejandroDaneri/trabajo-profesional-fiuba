from typing import List
from algo_lib.actions import Action
from algo_lib.exchange import Exchange
from strategies.strategy import Strategy

from trade import Trade 

class TradeBot:
    def __init__(self, strategy: Strategy, exchange: Exchange):
        self.strategy = strategy
        self.exchange = exchange
        self.trades = []

    def execute_trade(self, action: Action, symbol, amount):
        if action != Action.HOLD:
            trade = Trade(action, symbol, amount, self.exchange)

            try:
                self.exchange.place_order(trade)

                self.trades.append(trade)
            except Exception as e:
                print(f"Error al ejecutar el trade: {e}")

    def run_strategy(self, new_record):
        # Use the strategy to predict the action
        action = self.strategy.predict(new_record)

        # Example: Assume symbol is 'AAPL' and amount is 10
        symbol = 'AAPL'
        amount = 10

        # Execute the predicted action
        self.execute_trade(action, symbol, amount)

