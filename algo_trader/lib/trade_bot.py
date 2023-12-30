from lib.actions import Action
from lib.exchanges.exchange import Exchange
from lib.strategies.strategy import Strategy

from lib.trade import Trade

class TradeBot:
    def __init__(self, strategy: dict[Strategy], exchange: Exchange):
        self.strategy = strategy
        self.exchange = exchange
        self.trades = []
        self.stop_loss_ratio = 0.2

        self.current_trade = None

    def execute_trade(self, action: Action, symbol, amount: float, price: float, timestamp: int):
        if action != Action.HOLD:
            if action == Action.BUY:
                self.current_trade = Trade(symbol, amount, price, timestamp)
                self.exchange.place_order(self.current_trade, Action.BUY)
            if action == Action.SELL:
                self.current_trade.sell(price, timestamp)
                self.trades.append(self.current_trade)
                self.exchange.place_order(self.current_trade, Action.SELL)
                return_trade = self.current_trade
                self.current_trade = None
                return return_trade

    def run_strategy(self, currency, new_record):
        action = self.strategy[currency].predict(new_record)
        print(f'[Strategy] Signal: {action}')
        timestamp = new_record['Open time'].iloc[0]
        if (self.trades): 
            asset_last_value = new_record["Close"][0]

            # Check for stop-loss condition before executing a sell order
            if (
                self.current_trade is not None
                and self.current_trade.symbol == currency
                and asset_last_value < self.current_trade.buy_order.price * (1 - self.stop_loss_ratio)
            ):
                print("Stop-loss triggered. Selling...")
                trade = self.execute_trade(
                    Action.SELL,
                    currency,
                    self.exchange.portfolio[currency],
                    asset_last_value,
                    timestamp
                )
                return trade


        buy_condition = action == Action.BUY and (self.current_trade is None)
        sell_condition = action == Action.SELL and (self.current_trade is not None) and (self.current_trade.symbol == currency)

        asset_last_value = new_record["Close"][0]

        if buy_condition:
            max_buy_amount = self.strategy[currency].investment_ratio * self.exchange.balance / asset_last_value
            trade = self.execute_trade(
                Action.BUY,
                currency,
                max_buy_amount,
                asset_last_value,
                timestamp
            )
            return trade

        elif sell_condition:
            max_sell_amount = self.exchange.portfolio[currency] * self.strategy[currency].investment_ratio
            trade = self.execute_trade(
                Action.SELL,
                currency,
                max_sell_amount,
                asset_last_value,
                timestamp
            )
            return trade
        else:
            #print("Time to HODL")
            return None


    def get_trades(self):
        return self.trades
    
    def get_balance(self):
        return self.exchange.get_balance()
    
    def get_profit(self):
        return self.exchange.get_profit()
