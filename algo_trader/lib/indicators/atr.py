from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class ATR(Indicator):
    def __init__(self, rounds):
        self.rounds = rounds
        super().__init__("ATR")

    def calculate(self, data):
        # Calculate ATR (Average True Range)
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates= data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        df["HighLow"] = data["High"] - data["Low"]
        df["HighClose"] = abs(data["High"] - data["Close"].shift(1).fillna(0))
        df["LowClose"] = abs(data["Low"] - data["Close"].shift(1).fillna(0))

        df["TrueRange"] = df[["HighLow", "HighClose", "LowClose"]].max(axis=1, skipna=False)
        df["ATR"] = df["TrueRange"].ewm(span=self.rounds, min_periods=self.rounds).mean()

        # Drop innecesary columns
        df.drop(["HighLow", "HighClose", "LowClose", "TrueRange"], axis=1, inplace=True)

        self.output = df["ATR"]
        return self.output
    
    def plot(self):
        data = pd.DataFrame(self.output, index= self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data["ATR"], color='blue', linewidth=1)
        plt.grid()
        plt.show()
