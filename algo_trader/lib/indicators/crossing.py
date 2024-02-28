from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd


class Crossing(Indicator):
    def __init__(self, buy_threshold, sell_threshold, fast, slow):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.fast = fast
        self.slow = slow
        super().__init__("Cruce")

    def calculate(self, data, normalize=False):
        df = pd.DataFrame(index=data.index)
        self.data = data
        df["Close"] = data["Close"]
        df[self.name] = (
            df.Close.rolling(self.fast).mean() / df.Close.rolling(self.slow).mean() - 1
        )
        self.output = df[self.name]
        return super().calculate(data, normalize)

    def calc_sell_signals(self):
        return self._calc_sell_signals(self.output < self.sell_threshold)

    def calc_buy_signals(self):
        return self._calc_buy_signals(self.output > self.buy_threshold)

    def predict_signal(self, new_record):
        new_output = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_output.iloc[-1]

        print(f"[Crossing] Current value: {new_signal}")
        print(f"[Crossing] Sell Threshold: {self.sell_threshold}")
        print(f"[Crossing] Buy Threshold: {self.buy_threshold}")

        signal = self.get_last_signal(True)

        print(f"[Crossing] Signal: {signal}")

        return signal
