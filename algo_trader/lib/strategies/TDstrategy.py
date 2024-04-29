from lib.indicators.indicator import Indicator
from lib.strategies.strategy import Strategy
from algo_trader.lib.strategies.base_strategies.TrendDetectionBase import TrendDetectionBase
from typing import List

import pandas as pd
import numpy as np

class TDstrategy(Strategy):
    def __init__(self, indicators: List[Indicator], timeframe: str, id: str):
        self.name = "TD"

        # TODO: check to parameterize this data
        self.rounds_ema = 14
        self.rounds_dmi = 5
        self.threshold_adx = 20
        self.period_slope = 5
        self.tdb = TrendDetectionBase(self.rounds_ema, self.rounds_dmi, self.threshold_adx, self.period_slope)   

        super().__init__(indicators, timeframe, id)

    def prepare_data(self, historical_data: pd.DataFrame):
        print(self.name + " | begin prepare")
        self.data = historical_data[["Open", "High", "Low", "Close","Volume"]].copy()
        self.data["High"] = self.data["High"].apply(lambda x: float(x))
        self.data["Low"] = self.data["Low"].apply(lambda x: float(x))
        self.data["Close"] = self.data["Close"].apply(lambda x: float(x))
        self.data["Volume"] = self.data["Volume"].apply(lambda x: float(x))
        self.data["Open"] = self.data["Open"].apply(lambda x: float(x))

        confirmed_signals = self.tdb.get_confirmed_signals(self, self.data)
        
        for indicator in self.indicators:
            self.data[indicator.name] = None
            indicator.calculate(self.data, False)
            self.data[indicator.name] = np.where(indicator.generate_signals() == confirmed_signals, confirmed_signals, 0)
        
        print(self.name + " | end prepare")

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