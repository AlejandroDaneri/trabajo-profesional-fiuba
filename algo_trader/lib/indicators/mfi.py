from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class MFI(Indicator):
    def __init__(self, buy_threshold, sell_threshold, rounds):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.rounds = rounds
        super().__init__("MFI")

    def calculate(self, data, normalize=False):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Calculate the typical price, its is the average of the maximum, minimum and close price
        df["TP"] = (data["High"] + data["Low"] + data["Close"]) / 3

        # Calculate the money flow , its value is the result of TP * Volume
        df["MF"] = df["TP"] * data["Volume"]

        # Calculate the positive and negative money flows during N periods
        # Money flow positive = if TP > previous TP
        # Money flow negative = if TP < previous TP
        df["MF_Sign"] = np.where(df["TP"] > df["TP"].shift(1), 1, -1)
        df["Signed_MF"] = df["MF"] * df["MF_Sign"]

        df["MF+"] = np.where(df["Signed_MF"] > 0, df["Signed_MF"], 0)
        df["MF-"] = np.where(df["Signed_MF"] < 0, -df["Signed_MF"], 0)

        df["MF_Avg_Gain"] = df["MF+"].rolling(self.rounds).sum()
        df["MF_Avg_Loss"] = df["MF-"].rolling(self.rounds).sum()

        # Calculate the monetary ratio
        df["MR"] = df["MF_Avg_Gain"] / df["MF_Avg_Loss"]

        # Calculate the MFI
        df[self.name] = 100 - (100 / (1 + df["MR"]))

        self.output = df[self.name]
        return super().calculate(data, normalize)

    def calc_buy_signals(self):
        return self._calc_buy_signals(
            (self.output.shift(1) < self.buy_threshold)
            & (self.buy_threshold <= self.output)
        )

    def calc_sell_signals(self):
        return self._calc_sell_signals(
            (self.output.shift(1) > self.sell_threshold)
            & (self.sell_threshold >= self.output)
        )

    def plot(self):
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data[self.name], color="orange", linewidth=2)
        plt.grid()
        # Oversold
        plt.axhline(self.buy_threshold, linestyle="--", linewidth=1.5, color="green")
        # Overbought
        plt.axhline(self.sell_threshold, linestyle="--", linewidth=1.5, color="red")
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_mfi = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_mfi.iloc[-1]

        print(f"[MFI] Current value: {new_signal}")
        print(f"[MFI] Sell Threshold: {self.sell_threshold}")
        print(f"[MFI] Buy Threshold: {self.buy_threshold}")

        signal = self.get_last_signal(as_enum)

        print(f"[MFI] Signal: {signal}")

        return signal
