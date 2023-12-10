from lib.indicators.indicator import Indicator
from lib.strategies.strategy import Strategy

from collections import Counter
import pandas as pd
import numpy as np
from typing import List, Tuple

param_space = {
    "rsi_upper": (30, 70),
    "rsi_lower": (30, 70),
    "rsi_period": (5, 20),
    "crossing_threshold_buy": (-0.1, 0.1),
    "crossing_threshold_sell": (-0.1, 0.1),
    "crossing_short_window": (10, 50),
    "crossing_long_window": (50, 100),
}


class RandomSearch(Strategy):
    def __init__(self, indicators: List[Indicator]):
        self.name = "RS"
        super().__init__(indicators)

    def train(self, historical_data):
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

        return most_common_signal
