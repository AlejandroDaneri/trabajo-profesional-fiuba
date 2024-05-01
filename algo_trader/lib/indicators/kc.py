from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class KC(Indicator):
    def __init__(self, periods: int, atr_length: int, atr_ma: float, factor: float):
        self.periods = periods
        self.atr_length = atr_length
        self.atr_ma = atr_ma
        self.factor = factor
        super().__init__("KC")

    def calculate(self, data):
        self.data = data
        df = pd.DataFrame(index=data.index)
        df["Close"] = data["Close"]
        df["ATR"] = data["High"] - data["Low"]
        df["MA_ATR"] = df["ATR"].rolling(self.atr_length).mean()
        df["UpperBand"] = data["Close"].rolling(self.periods).mean() + self.atr_ma * df["MA_ATR"]
        df["LowerBand"] = data["Close"].rolling(self.periods).mean() - self.atr_ma * df["MA_ATR"]
        self.df_output = df.fillna(0)
        return self.df_output

    def calc_buy_signals(self):
        return (self.df_output["Close"] < self.df_output["LowerBand"]*(1 + self.factor)) & (self.df_output["Close"] > self.df_output["LowerBand"])

    def calc_sell_signals(self):
        return (self.df_output["Close"] > self.df_output["UpperBand"]*(1 - self.factor)) & (self.df_output["Close"] < self.df_output["UpperBand"])

    def plot(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data["Close"], label="Close Price")
        plt.plot(self.df_output.index, self.df_output["UpperBand"], label="Upper Keltner Channel", linestyle="--")
        plt.plot(self.df_output.index, self.df_output["LowerBand"], label="Lower Keltner Channel", linestyle="--")
        plt.title("Keltner Channels (KC) Indicator")
        plt.legend()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_data = pd.concat([self.data, new_record])
        new_kc_value = self.calculate(new_data).iloc[-1]

        if new_data["Close"].iloc[-1] < new_kc_value["LowerBand"]:
            signal = "BUY"
        elif new_data["Close"].iloc[-1] > new_kc_value["UpperBand"]:
            signal = "SELL"
        else:
            signal = "HOLD"

        if as_enum:
            return IndicatorSignal.BUY if signal == "BUY" else IndicatorSignal.SELL if signal == "SELL" else IndicatorSignal.HOLD
        else:
            return signal
        
    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        signal = self.get_last_signal(as_enum)
        return signal
