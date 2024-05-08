from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class SMA(Indicator):
    def __init__(self, rounds:int):
        self.rounds = rounds
        super().__init__("SMA")

    def calculate(self, data, normalize=False):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        # Calculate the average of the last n rounds of close
        df["SMA"] = data["Close"].rolling(self.rounds).mean()

        self.df_output = df
        return self.df_output

    def calc_buy_signals(self):
        return self._calc_buy_signals(
            (self.df_output.Close.shift(1) < self.df_output.SMA.shift(1))
            & (self.df_output.SMA <= self.df_output.Close)
        )

    def calc_sell_signals(self):
        return self._calc_sell_signals(
            (self.df_output.SMA.shift(1) < self.df_output.Close.shift(1))
            & (self.df_output.Close <= self.df_output.SMA)
        )

    def plot(self):
        data = pd.DataFrame(self.df_output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data.index, data.SMA, color="green", linewidth=1)
        plt.plot(data.index, data.Close, color="blue", linewidth=1)
        plt.grid()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        print(f"[SMA] Current SMA value: {new_signal.SMA}")
        print(f"[SMA] Current Close value: {new_signal.Close}")

        signal = self.get_last_signal(as_enum)

        print(f"[SMA] Signal: {signal}")

        return signal