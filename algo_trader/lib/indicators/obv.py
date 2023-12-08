from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class OBV(Indicator):
    def __init__(self, n, buy_threshold, sell_threshold):
        self.n = n
        super().__init__("OBV", buy_threshold, sell_threshold)

    def calculate(self, data):
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        df["Balance"] = np.where(
            data.Close > data.Close.shift(),
            data["Volume"],
            np.where(data.Close < data.Close.shift(), -data["Volume"], 0),
        )
        df[self.name] = df["Balance"].rolling(self.n).sum()
        self.output = df[self.name]

        return self.output

    def calc_buy_signals(self):
        # Generate buy signals when OBV crosses above the buy threshold
        return np.where(self.output > self.buy_threshold, True, False)

    def calc_sell_signals(self):
        # Generate sell signals when OBV crosses below the sell threshold
        return np.where(self.output < self.sell_threshold, True, False)

    def plot(self):
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data[self.name])
        plt.show()

    def predict_signal(self, new_record):
        # Calculate OBV for the updated DataFrame
        new_obv = self.calculate(pd.concat([self.data, new_record]))

        # Extract the value of OBV for the new record
        new_signal = new_obv.iloc[-1]

        # Trading decisions based on OBV signals
        if new_signal > self.buy_threshold:
            return Action.BUY
        elif new_signal < self.sell_threshold:
            return Action.SELL
        else:
            return Action.HOLD
