from lib.indicators.indicator import Indicator
from lib.actions import Action
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class MACD(Indicator):
    def __init__(self, slow: int, fast: int, smoothed: int):
        self.slow = slow
        self.fast = fast
        self.smoothed = smoothed
        super().__init__("MACD")

    def calculate(self, data, normalize=False):
        self.data = data
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
        df["signal"] = df.macd.ewm(span=self.smoothed).mean()

        # Finally, the point of interest is the difference between the MACD and the signal
        # It is particularly interesting when it crosses zero.
        df["histogram"] = df.macd - df.signal

        # Drop any NaN values and round the DataFrame to two decimal places
        df = df.dropna().round(2)

        # Rename the 'histogram' column with the indicator name for convenience (notation abuse)
        self.output = df
        return super().calculate(data, normalize)

    def calc_buy_signals(self):
        return self._calc_buy_signals((self.output["histogram"].shift(1) < 0) & (0 < self.output["histogram"]))

    def calc_sell_signals(self):
        return self._calc_sell_signals((self.output["histogram"].shift(1) > 0) & (0 >= self.output["histogram"]))

    def plot(self):
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data["histogram"])
        plt.grid()
        plt.axhline(0, linestyle="--", linewidth=1.5, color="black")
        plt.fill_between(
            data.index, data["histogram"], 0, where=data["histogram"] > 0, alpha=0.5, color="green"
        )
        plt.fill_between(
            data.index, data["histogram"], 0, where=data["histogram"] < 0, alpha=0.5, color="red"
        )
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_macd_value = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_macd_value.iloc[-1]

        print(f"[MACD] Current value: {new_signal}")

        signal = self.get_last_signal(as_enum)

        print(f"[MACD] Signal: {signal}")

        return signal