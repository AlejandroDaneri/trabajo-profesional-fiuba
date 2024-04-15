from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class ROC(Indicator):
    def __init__(self, periods):
        self.periods = periods
        super().__init__("ROC")

    def calculate(self, data):
        self.data = data
        df = pd.DataFrame(index=data.index)
        df["ROC"] = (data["Close"] - data["Close"].shift(self.periods)) / data["Close"].shift(self.periods)
        self.df_output = df.dropna()
        return self.df_output

    def calc_buy_signals(self, threshold=0):
        return self.df_output["ROC"] > threshold

    def calc_sell_signals(self, threshold=0):
        return self.df_output["ROC"] < threshold

    def plot(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.df_output.index, self.df_output["ROC"], label=f"ROC ({self.periods} periods)")
        plt.axhline(0, color='black', linestyle='--')
        plt.title("Rate of Change (ROC) Indicator")
        plt.legend()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        signal = self.get_last_signal(as_enum)
        return signal

