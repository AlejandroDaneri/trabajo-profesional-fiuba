from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class EWO(Indicator):
    def __init__(self, short_period: int=10, long_period: int=25):
        self.short_period = short_period
        self.long_period = long_period
        super().__init__("EWO")

    def calculate(self, data):
        self.data = data
        df = pd.DataFrame(index=data.index)
        ema_short = data["Close"].ewm(span=self.short_period, adjust=False).mean()
        ema_long = data["Close"].ewm(span=self.long_period, adjust=False).mean()
        df["EWO"] = ema_short - ema_long
        self.df_output = df.fillna(0)
        return self.df_output

    def calc_buy_signals(self):
        return self.df_output["EWO"] > 0

    def calc_sell_signals(self):
        return self.df_output["EWO"] < 0

    def plot(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.df_output.index, self.df_output["EWO"], label=f"EWO ({self.short_period},{self.long_period})")
        plt.axhline(0, color='black', linestyle='--')
        plt.title("Elliott Wave Oscillator (EWO) Indicator")
        plt.legend()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        signal = self.get_last_signal(as_enum)
        return signal
