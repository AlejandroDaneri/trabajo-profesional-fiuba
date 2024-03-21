from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Stochastic(Indicator):
    def __init__(self, buy_threshold, sell_threshold, rounds, d_period=3):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.rounds = rounds
        self.d_period = d_period
        super().__init__("Stochastic")

    def calculate(self, data, normalize=False):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        # Calculate the max value of High of previous N periods
        df["Max_high"] = data["High"].rolling(self.rounds).max()

        # Calculate the min value of Low of previous N periods
        df["Min_low"] = data["Low"].rolling(self.rounds).min()

        # Uses the min/max values to calculate the %k (as a percentage)
        df["%K"] = (
            (df["Close"] - df["Min_low"]) * 100 / (df["Max_high"] - df["Min_low"])
        )

        # Uses the %k to calculates a SMA over the past 'd_period' values of %k (recommended value is 3)
        df["%D"] = df["%K"].rolling(self.d_period).mean()

        # Drop innecesary columns
        df.drop(["Min_low", "Max_high"], axis=1, inplace=True)

        self.output = df
        return super().calculate(data, normalize)

    def calc_buy_signals(self):
        return self._calc_buy_signals(
            (self.output["%K"].shift(1) < self.output["%D"].shift(1))
            & (self.output["%D"] <= self.output["%K"])
            & (self.output["%K"] <= self.buy_threshold)
            & (self.output["%D"] <= self.buy_threshold)
        )

    def calc_sell_signals(self):
        return self._calc_sell_signals(
            (self.output["%K"].shift(1) > self.output["%D"].shift(1))
            & (self.output["%D"] >= self.output["%K"])
            & (self.output["%K"] >= self.sell_threshold)
            & (self.output["%D"] >= self.sell_threshold)
        )

    def plot(self):
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data["%K"], color="blue", linewidth=1)
        plt.plot(data["%D"], color="orange", linewidth=1)
        plt.grid()
        # Oversold
        plt.axhline(self.buy_threshold, linestyle="--", linewidth=1.5, color="green")
        # Overbought
        plt.axhline(self.sell_threshold, linestyle="--", linewidth=1.5, color="red")
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_stoch = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_stoch.iloc[-1]

        print(f"[Stochastic] Current value: {new_signal}")
        print(f"[Stochastic] Sell Threshold: {self.sell_threshold}")
        print(f"[Stochastic] Buy Threshold: {self.buy_threshold}")

        signal = self.get_last_signal(as_enum)

        print(f"[Stochastic] Signal: {signal}")

        return signal
