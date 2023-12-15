from lib.actions import Action
from lib.exchanges.exchange import Exchange
from lib.strategies.strategy import Strategy

from lib.trade import Trade

class TradeBot:
    def __init__(self, strategy: Strategy, exchange: Exchange, symbol: str):
        self.strategy = strategy
        self.exchange = exchange
        self.symbol = symbol
        self.trades = []
        self.stop_loss_ratio = 0.2

    def execute_trade(self, action: Action, symbol, amount: float, price: float):
        if action != Action.HOLD:
            trade = Trade(action, symbol, amount, price)
            try:
                self.exchange.place_order(trade)
                self.trades.append(trade)
                return trade
            except Exception as e:
                print(f"Error executing trade: {e}")

    def run_strategy(self, new_record):
        action = self.strategy.predict(new_record)
        if (self.trades): 
            last_action = self.trades[-1].action
            last_trade_price = self.trades[-1].price
            asset_last_value = new_record["Close"][0]

            # Check for stop-loss condition before executing a sell order
            if (
                last_action == Action.BUY
                and asset_last_value < last_trade_price * (1 - self.stop_loss_ratio)
            ):
                print("Stop-loss triggered. Selling...")
                trade = self.execute_trade(
                    Action.SELL,
                    self.symbol,
                    self.exchange.portfolio[self.symbol],
                    asset_last_value,
                )
                return trade

        buy_condition = action == Action.BUY and (not self.trades or last_action == Action.SELL)
        sell_condition = self.trades and action == Action.SELL and last_action == Action.BUY
        asset_last_value = new_record["Close"][0]

        if buy_condition:
            max_buy_amount = self.strategy.investment_ratio * self.exchange.balance / asset_last_value
            trade = self.execute_trade(
                Action.BUY,
                self.symbol,
                max_buy_amount,
                asset_last_value,
            )
            return trade

        elif sell_condition:
            max_sell_amount = self.exchange.portfolio[self.symbol] * self.strategy.investment_ratio
            trade = self.execute_trade(
                Action.SELL,
                self.symbol,
                max_sell_amount,
                asset_last_value,
            )
            return trade
        else:
            print("Time to HODL")
            return None


    def get_trades(self):
        return self.trades
    
    def get_profit(self):
        return self.exchange.get_profit()
