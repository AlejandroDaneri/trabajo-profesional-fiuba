from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class BBANDS(Indicator):
    def __init__(self, rounds:int = 9, factor:float=2.1):
        # Moving Average periods
        self.rounds = rounds
        # Factor to shift the bands
        self.factor = factor
        super().__init__("BBANDS")

    def calculate(self, data, normalize=False):
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the DataFrame
        df["Close"] = data["Close"]

        # Calculate the average of the last n rounds of Close
        df["MidBand"] = data["Close"].rolling(self.rounds).mean()

        # Calculate the Standard Deviation of the last n rounds of Close
        df["Std"] = data["Close"].rolling(self.rounds).std()

        # Calculate the upper band
        df["UpperBand"] = df["MidBand"] + df["Std"] * self.factor

        # Calculate the lower band
        df["LowerBand"] = df["MidBand"] - df["Std"] * self.factor

        self.df_output = df
        return self.df_output

    def calc_buy_signals(self):
        return self._calc_buy_signals(self.df_output.Close <= self.df_output.LowerBand)

    def calc_sell_signals(self):
        return self._calc_sell_signals(self.df_output.Close >= self.df_output.UpperBand)

    def plot(self):
        data = self.df_output

        fig = plt.figure()
        fig.set_size_inches(16, 8)
        plt.plot(data.index, data.Close)
        plt.plot(data.index, data.MidBand, linewidth=0.5, linestyle="dashed")
        plt.plot(data.index, data.UpperBand, linewidth=0.5, color="#033660")
        plt.plot(data.index, data.LowerBand, linewidth=0.5, color="#033660")
        plt.grid()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_bbands_value = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_bbands_value.iloc[-1]

        print(f"[BBANDS] Current value: {new_signal.Close}")
        print(f"[BBANDS] UpperBand value: {new_signal.UpperBand}")
        print(f"[BBANDS] LowerBand value: {new_signal.LowerBand}")

        signal = self.get_last_signal(as_enum)

        print(f"[BBANDS] Signal: {signal}")

        return signal