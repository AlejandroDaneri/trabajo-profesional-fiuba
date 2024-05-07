import pandas as pd
import numpy as np
from typing import Tuple

class BuyAndHoldBacktester:
    def __init__(self, initial_balance: float, historical_data: pd.DataFrame, fixed_commission: float=0.005, variable_commission_rate: float=0.005):
        self.initial_balance = initial_balance
        self.historical_data = historical_data
        self.fixed_commission = fixed_commission
        self.variable_commission_rate = variable_commission_rate
        self.strat_lin = None
        self.strat = None
        self.benchmark = None
        self.strat_log = None
        self.benchmark_log = None

    def backtest(self) -> Tuple[pd.DataFrame, float]:
        trades, final_balance = self._execute_backtest()
        return trades, final_balance

    def _execute_backtest(self) -> Tuple[pd.DataFrame, float]:
        buy_price = self.historical_data.iloc[0]["Close"]
        sell_price = self.historical_data.iloc[-1]["Close"]
        final_balance = (sell_price / buy_price) * self.initial_balance

        # Calcula las variables estratégicas y guárdalas en self
        pct_change = self.historical_data['Close'].pct_change()
        self.strat_lin = pct_change
        self.strat = (1 + self.strat_lin).cumprod()
        self.benchmark = pct_change.add(1).cumprod()

        self.strat_log = np.log(self.strat / self.strat.shift())
        self.benchmark_log = np.log(self.benchmark / self.benchmark.shift())

        trades = pd.DataFrame({
            "buy_date": [self.historical_data.index[0]],
            "buy_price": [buy_price],
            "sell_date": [self.historical_data.index[-1]],
            "sell_price": [sell_price],
            "fixed_commission": [self.fixed_commission],
            "variable_commission": [buy_price * self.variable_commission_rate],
            "return": [(sell_price / buy_price) - 1],
            "cumulative_return": [final_balance / self.initial_balance - 1],
            "result": ["Winner" if (sell_price / buy_price) > 1 else "Loser"]
        })

        return trades, final_balance