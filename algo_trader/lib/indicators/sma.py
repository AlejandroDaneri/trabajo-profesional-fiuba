from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class SMA(Indicator):
    def __init__(self, fast_rounds, slow_rounds):
        self.fast_rounds = fast_rounds
        self.slow_rounds = slow_rounds
        super().__init__("SMA")

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

        self.df_output = df
        return self.df_output

    def calc_buy_signals(self):
        return np.where(
            (self.df_output.FAST_SMA.shift(1) < self.df_output.SLOW_SMA.shift(1))
            & (self.df_output.SLOW_SMA <= self.df_output.FAST_SMA),
            True,
            False,
        )

    def calc_sell_signals(self):
        return np.where(
            (self.df_output.SLOW_SMA.shift(1) < self.df_output.FAST_SMA.shift(1))
            & (self.df_output.FAST_SMA <= self.df_output.SLOW_SMA),
            True,
            False,
        )

    def plot(self):
        data = pd.DataFrame(self.df_output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data.index, data.FAST_SMA, color="green", linewidth=1)
        plt.plot(data.index, data.SLOW_SMA, color="red", linewidth=1)
        plt.grid()
        plt.show()

    def predict_signal(self, new_record):
        new_df = self.calculate(pd.concat([self.data, new_record]))
        sell_signal = self.calc_sell_signals()[-1]
        buy_signal = self.calc_buy_signals()[-1]

        new_signal = new_df.iloc[-1]

        print(f"[SMA] Current fast SMA value: {new_signal.FAST_SMA}")
        print(f"[SMA] Current slow SMA value: {new_signal.SLOW_SMA}")

        if sell_signal == True:
            signal = Action.SELL
        elif buy_signal == True:
            signal = Action.BUY
        else:
            signal = Action.HOLD

        print(f"[SMA] Signal: {signal}")

        return signal
