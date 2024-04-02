from lib.actions import Action
from lib.indicators.indicator import Indicator
from lib.utils.plotter import plot_df

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fuente: https://www.lookintobitcoin.com/charts/pi-cycle-top-indicator

class PiCycleTop(Indicator):
    def __init__(self):
        super().__init__("PiCycleTop")

    def calculate(self, data, normalize=False):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        df["Close"] = data["Close"]
        df["MA_111"] = df["Close"].rolling(111).mean()
        df["MA_350_x2"] = df["Close"].rolling(350).mean() * 2

        self.df_output = df
        return self.df_output

    def calc_buy_signals(self):
        df = self.df_output
        # fast > slow & fast < slow
        buy_condition = (df.MA_111.shift(1) > df.MA_350_x2.shift(1)) & (df.MA_111 <= df.MA_350_x2)
        return self._calc_buy_signals(buy_condition)

    def calc_sell_signals(self):
        df = self.df_output
        # fast < slow & fast > slow
        sell_condition = (df.MA_111.shift(1) < df.MA_350_x2.shift(1)) & (df.MA_111 > df.MA_350_x2)
        return self._calc_sell_signals(sell_condition)

    def plot(self, log_scale=False):
        df = self.df_output
        plot_df(self.data.index, df, log_scale=log_scale)

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        print(f"[Crossing SMA] Current fast SMA value: {new_signal.FAST_SMA}")
        print(f"[Crossing SMA] Current slow SMA value: {new_signal.SLOW_SMA}")

        signal = self.get_last_signal(as_enum)

        print(f"[Crossing SMA] Signal: {signal}")

        return signal
