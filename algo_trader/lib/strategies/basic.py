from lib.indicators.indicator import Indicator
from lib.strategies.strategy import Strategy

from collections import Counter
import pandas as pd
import numpy as np
from typing import List, Tuple


class Basic(Strategy):
    def __init__(self, indicators: List[Indicator], timeframe: str, id: str):
        self.name = "BASIC"
        super().__init__(indicators, timeframe, id)

    def prepare_data(self, historical_data):
        for indicator in self.indicators:
            indicator.calculate(historical_data)
        return

    def predict(self, new_record):
        # List to store predicted signals from each indicator
        signals = []

        # Get predicted signals from each indicator
        for indicator in self.indicators:
            signal = indicator.predict_signal(new_record)
            signals.append(signal)

        # Count the frequency of each signal
        signal_counter = Counter(signals)

        # Get the most common signal
        most_common_signal = signal_counter.most_common(1)[0][0]

        print(f'[Strategy | Basic] Signal: {most_common_signal}')

        return most_common_signal

    # def execute_backtest(self, historical_data: pd.DataFrame,initial_balance, fixed_commission,variable_commission_rate) -> Tuple[pd.DataFrame, float]:
    #     buy_signals, sell_signals = self.get_buy_sell_signals(historical_data)

    #     actions = self._get_actions(buy_signals, sell_signals)
    #     historical_data['signal'] = actions['signal'] 

    #     trades = self._get_trades(actions,fixed_commission,variable_commission_rate)
    #     self.payoff= self._event_drive(historical_data)
    #     final_balance = self._calculate_final_balance(historical_data, trades, initial_balance)

    #     return trades, final_balance

    def get_buy_sell_signals(self, historical_data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        buy_signals = pd.DataFrame(index=historical_data.index)
        sell_signals = pd.DataFrame(index=historical_data.index)
        buy_signals["Close"] = historical_data["Close"]
        sell_signals["Close"] = historical_data["Close"]

        for indicator in self.indicators:
            indicator.calculate(historical_data)
            buy_signals[indicator.name] = np.where(indicator.calc_buy_signals(), 1, 0)
            sell_signals[indicator.name] = np.where(indicator.calc_sell_signals(), 1, 0)

        return buy_signals, sell_signals

