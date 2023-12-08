from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MACD(Indicator):
    def __init__(self, slow, fast, suavizado):
        self.slow = slow
        self.fast = fast
        self.suavizado = suavizado
        super().__init__("MACD", 0, 0)

    def calculate(self, data):
        df = pd.DataFrame(index=data.index)
        self.dates = data.index
        # Copy the 'Close' column from the original data to the DataFrame
        df["Close"] = data["Close"]

        # Calculate the fast exponential moving average
        df["ema_fast"] = df.Close.ewm(span=self.fast).mean()

        # Calculate the slow exponential moving average
        df["ema_slow"] = df.Close.ewm(span=self.slow).mean()

        # The difference between the fast and slow moving averages is another moving average called MACD
        df["macd"] = df.ema_fast - df.ema_slow

        # Smooth the MACD and call it the 'signal'
        df["signal"] = df.macd.ewm(span=self.suavizado).mean()

        # Finally, the point of interest is the difference between the MACD and the signal
        # It is particularly interesting when it crosses zero.
        df["histogram"] = df.macd - df.signal

        # Drop any NaN values and round the DataFrame to two decimal places
        df = df.dropna().round(2)

        # Rename the 'histogram' column with the indicator name for convenience (notation abuse)
        df[self.name] = df["histogram"]
        self.output = df[self.name]
        return self.output

    def calc_buy_signals(self):
        # Find where the MACD line crosses above the signal line
        return np.where((self.output > 0) & (self.output.shift(1) <= 0), True, False)

    def calc_sell_signals(self):
        # Find where the MACD line crosses below the signal line
        return np.where((self.output < 0) & (self.output.shift(1) >= 0), True, False)

    def plot(self):
        # TODO: fix plot
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data[self.name])
        plt.show()
