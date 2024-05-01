from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class DONCHIAN(Indicator):
    def __init__(self, periods: int, factor: float):
        self.periods = periods
        self.factor = factor
        super().__init__("DONCHIAN")

    def calculate(self, data):
        self.data = data
        df = pd.DataFrame(index=data.index)
        df["Close"] = data["Close"]
        df["HighChannel"] = data["High"].rolling(self.periods).max()
        df["LowChannel"] = data["Low"].rolling(self.periods).min()
        df["MidChannel"] = (df["HighChannel"] + df["LowChannel"]) / 2
        self.df_output = df.fillna(0)
        return self.df_output

    def calc_buy_signals(self):
        return (self.df_output["Close"] < self.df_output["LowChannel"]*(1 + self.factor)) & (self.df_output["Close"] > self.df_output["LowChannel"])

    def calc_sell_signals(self):
        return (self.df_output["Close"] > self.df_output["HighChannel"]*(1 - self.factor)) & (self.df_output["Close"] < self.df_output["HighChannel"])

    def plot(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data["Close"], label="Close Price")
        plt.plot(self.df_output.index, self.df_output["HighChannel"], label="Upper Donchian Channel", linestyle="--")
        plt.plot(self.df_output.index, self.df_output["LowChannel"], label="Lower Donchian Channel", linestyle="--")
        plt.title("Donchian Channels Indicator")
        plt.legend()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        signal = self.get_last_signal(as_enum)
        return signal
