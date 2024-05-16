import pandas as pd
import numpy as np
from typing import Tuple

class BuyAndHoldBacktester:
    def __init__(self, initial_balance: float, historical_data: pd.DataFrame):
        self.initial_balance = initial_balance
        self.historical_data = historical_data

    def backtest(self) -> Tuple[pd.DataFrame, float]:
        trades, final_balance = self._execute_backtest()
        return trades, final_balance

    def _execute_backtest(self) -> Tuple[pd.DataFrame, float]:
        buy_price = self.historical_data.iloc[0]["Close"]
        sell_price = self.historical_data.iloc[-1]["Close"]
        final_balance = (sell_price / buy_price) * self.initial_balance

        pct_change = self.historical_data['Close'].pct_change()
        self.strategy_linear_returns = pct_change
        self.strategy_returns = (1 + self.strategy_linear_returns).cumprod()
        self.benchmark_returns = pct_change.add(1).cumprod()

        self.strategy_log_returns = np.log(self.strategy_returns / self.strategy_returns.shift())
        self.benchmark_log_returns = np.log(self.benchmark_returns / self.benchmark_returns.shift())

        trades = pd.DataFrame({
            "buy_date": [self.historical_data.index[0]],
            "buy_price": [buy_price],
            "sell_date": [self.historical_data.index[-1]],
            "sell_price": [sell_price],
            "return": [(sell_price / buy_price) - 1],
            "cumulative_return": [final_balance / self.initial_balance - 1],
        })

        return trades, final_balance
