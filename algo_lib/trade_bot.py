from actions import Action
from exchanges.exchange import Exchange
from strategies.strategy import Strategy

from trade import Trade

class TradeBot:
    def __init__(self, strategy: Strategy, exchange: Exchange, symbol: str):
        self.strategy = strategy
        self.exchange = exchange
        self.symbol = symbol
        self.trades = []

    def execute_trade(self, action: Action, symbol, amount: float, price: float):
        if action != Action.HOLD:
            trade = Trade(action, symbol, amount, price)
            try:
                self.exchange.place_order(trade)
                self.trades.append(trade)
            except Exception as e:
                print(f"Error executing trade: {e}")

    def run_strategy(self, new_record):
        action = self.strategy.predict(new_record)
        if (self.trades): last_action = self.trades[-1].action
        buy_condition = action == Action.BUY and (not self.trades or last_action == Action.SELL)
        sell_condition = self.trades and action == Action.SELL and last_action == Action.BUY
        asset_last_value = new_record["Close"][0]

        if buy_condition:
            max_buy_amount = self.strategy.investment_ratio * self.exchange.balance / asset_last_value
            self.execute_trade(
                Action.BUY,
                self.symbol,
                max_buy_amount,
                asset_last_value,
            )

        elif sell_condition:
            max_sell_amount = self.exchange.portfolio[self.symbol] * self.strategy.investment_ratio
            self.execute_trade(
                Action.SELL,
                self.symbol,
                max_sell_amount,
                asset_last_value,
            )


    def get_trades(self):
        return self.trades
    
    def get_profit(self):
        return self.exchange.get_profit()
