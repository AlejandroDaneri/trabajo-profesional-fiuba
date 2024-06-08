from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class VWAP(Indicator):
    def __init__(self, periods: int=14):
        self.periods = periods
        super().__init__("VWAP")

    def calculate(self, data, normalize=False):
        self.data = data
        df = pd.DataFrame(index=data.index)
        df["Close"] = data["Close"]
        df["TypicalPrice"] = (data["High"] + data["Low"] + data["Close"]) / 3
        df["CumulativeTypicalPrice"] = (df["TypicalPrice"] * data["Volume"]).cumsum()
        df["CumulativeVolume"] = data["Volume"].cumsum()
        df["VWAP"] = df["CumulativeTypicalPrice"] / df["CumulativeVolume"]
        self.df_output = df.fillna(0)
        return self.df_output

    def calc_buy_signals(self):
        return self.df_output["Close"] > self.df_output["VWAP"]

    def calc_sell_signals(self):
        return self.df_output["Close"] < self.df_output["VWAP"]

    def plot(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.df_output.index, self.df_output["Close"], label="Close Price")
        plt.plot(self.df_output.index, self.df_output["VWAP"], label="VWAP", linestyle="--")
        plt.title("VWAP Indicator")
        plt.legend()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        signal = self.get_last_signal(as_enum)
        return signal

