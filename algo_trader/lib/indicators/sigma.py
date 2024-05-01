from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd


class Sigma(Indicator):
    def __init__(self, rounds:int =14):
        self.rounds = rounds
        super().__init__("Sigma")

    def calculate(self, data, normalize=False):
        df = pd.DataFrame(index=data.index)
        df["Close"] = data["Close"]
        df[self.name] = df.Close.pct_change().rolling(self.rounds).std()
        self.output = df[self.name]
        return super().calculate(data, normalize)

    def calc_buy_signals(self):
        return self._calc_buy_signals(self.output > 0.01)

    def calc_sell_signals(self):
        return self._calc_sell_signals(self.output < 55)
