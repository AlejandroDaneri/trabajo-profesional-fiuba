from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class ThreeSMA(Indicator):
    def __init__(self, fast_rounds: int, slow_rounds: int, support_rounds: int):
        self.fast_rounds = fast_rounds
        self.slow_rounds = slow_rounds
        self.support_rounds = support_rounds
        super().__init__("ThreeSMA")

    def calculate(self, data, normalize=False):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        # Calculate the fast average of the last n rounds of close
        df["FAST_SMA"] = data["Close"].rolling(self.fast_rounds).mean()

        # Calculate the slow average of the last n rounds of close
        df["SLOW_SMA"] = data["Close"].rolling(self.slow_rounds).mean()

        # Calculate the support average of the last n rounds of close
        df["SUPPORT_SMA"] = data["Close"].rolling(self.support_rounds).mean()

        self.df_output = df
        return self.df_output

    def calc_buy_signals(self):
        return self._calc_buy_signals(
            (self.df_output.FAST_SMA.shift(1) < self.df_output.SLOW_SMA.shift(1))
            & (self.df_output.SLOW_SMA <= self.df_output.FAST_SMA)
            & (self.df_output.SUPPORT_SMA >= self.df_output.SLOW_SMA)
            & (self.df_output.SUPPORT_SMA >= self.df_output.FAST_SMA)
        )

    def calc_sell_signals(self):
        return self._calc_sell_signals(
            (self.df_output.SLOW_SMA.shift(1) < self.df_output.FAST_SMA.shift(1))
            & (self.df_output.FAST_SMA <= self.df_output.SLOW_SMA)
            & (self.df_output.SUPPORT_SMA <= self.df_output.SLOW_SMA)
            & (self.df_output.SUPPORT_SMA <= self.df_output.FAST_SMA)
        )

    def plot(self):
        data = pd.DataFrame(self.df_output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data.index, data.FAST_SMA, color="green", linewidth=1)
        plt.plot(data.index, data.SLOW_SMA, color="red", linewidth=1)
        plt.plot(data.index, data.SUPPORT_SMA, color="orange", linewidth=1)
        plt.grid()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        print(f"[Three SMA] Current fast SMA value: {new_signal.FAST_SMA}")
        print(f"[Three SMA] Current slow SMA value: {new_signal.SLOW_SMA}")
        print(f"[Three SMA] Current support SMA value: {new_signal.SUPPORT_SMA}")

        signal = self.get_last_signal(as_enum)

        print(f"[Three SMA] Signal: {signal}")

        return signal