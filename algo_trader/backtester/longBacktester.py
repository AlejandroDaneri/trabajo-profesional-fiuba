from lib.strategies.strategy import Strategy
import pandas as pd
import numpy as np
from typing import Tuple

class LongBacktester:
    def __init__(self, strategy: Strategy, initial_balance: float, fixed_commission: float=0.005, variable_commission_rate: float=0.005):        
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.fixed_commission = fixed_commission
        self.variable_commission_rate = variable_commission_rate

    def backtest(self, historical_data: pd.DataFrame) -> Tuple[pd.DataFrame, float]:
        trades, final_balance = self.strategy.execute_backtest(historical_data,self.initial_balance,self.fixed_commission,self.variable_commission_rate)
        return trades, final_balance

    