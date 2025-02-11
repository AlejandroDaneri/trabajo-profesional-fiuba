from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class ThreeEMA(Indicator):
    def __init__(self, fast_rounds: int, slow_rounds: int, support_rounds: int):
        self.fast_rounds = fast_rounds
        self.slow_rounds = slow_rounds
        self.support_rounds = support_rounds
        super().__init__("ThreeEMA")

    def calculate(self, data, normalize=False):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        # Calculate the fast average of the last n rounds of close
        df["FAST_EMA"] = data["Close"].ewm(span=self.fast_rounds, adjust=False).mean()

        # Calculate the slow average of the last n rounds of close
        df["SLOW_EMA"] = data["Close"].ewm(span=self.slow_rounds, adjust=False).mean()

        # Calculate the support average of the last n rounds of close
        df["SUPPORT_EMA"] = (
            data["Close"].ewm(span=self.support_rounds, adjust=False).mean()
        )

        self.df_output = df
        return self.df_output

    def calc_buy_signals(self):
        return self._calc_buy_signals(
            (self.df_output.FAST_EMA.shift(1) < self.df_output.SLOW_EMA.shift(1))
            & (self.df_output.SLOW_EMA <= self.df_output.FAST_EMA)
            & (self.df_output.SUPPORT_EMA >= self.df_output.SLOW_EMA)
            & (self.df_output.SUPPORT_EMA >= self.df_output.FAST_EMA)
        )

    def calc_sell_signals(self):
        return self._calc_sell_signals(
            (self.df_output.SLOW_EMA.shift(1) < self.df_output.FAST_EMA.shift(1))
            & (self.df_output.FAST_EMA <= self.df_output.SLOW_EMA)
            & (self.df_output.SUPPORT_EMA <= self.df_output.SLOW_EMA)
            & (self.df_output.SUPPORT_EMA <= self.df_output.FAST_EMA)
        )

    def plot(self):
        data = pd.DataFrame(self.df_output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data.index, data.FAST_EMA, color="green", linewidth=1)
        plt.plot(data.index, data.SLOW_EMA, color="red", linewidth=1)
        plt.plot(data.index, data.SUPPORT_EMA, color="orange", linewidth=1)
        plt.grid()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        print(f"[Three EMA] Current fast EMA value: {new_signal.FAST_EMA}")
        print(f"[Three EMA] Current slow EMA value: {new_signal.SLOW_EMA}")
        print(f"[Three EMA] Current support EMA value: {new_signal.SUPPORT_EMA}")

        signal = self.get_last_signal(as_enum)

        print(f"[Three EMA] Signal: {signal}")

        return signal