from collections import Counter
from indicators.indicator import Indicator
from typing import List
from strategies.strategy import Strategy

class Basic(Strategy):
    def __init__(self, indicators: List[Indicator]):
        self.name = "BASIC"
        self.indicators = indicators


    def train(self,historical_data):
        ##TODO: modify this to save trades, actions, etc.
        for indicator in self.indicators:
            indicator.calculate(historical_data)
        return
    
    def predict(self,new_record):
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