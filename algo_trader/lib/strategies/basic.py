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
