from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class PVI(Indicator):
    def __init__(self, rounds):
        self.rounds = rounds
        super().__init__("PVI")

    def calculate(self, data, normalize=False):
        # Disable SettingWithCopyWarning
        pd.options.mode.chained_assignment = None

        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        # Calculate the difference in volume between the current and previous rows
        df["vol_diff"] = data["Volume"].diff()

        # Initialize PVI column in zero
        df["PVI"] = 0.0

        # Calculate each PVI value based on its previous PVI value
        for index in range(len(df)):
            if index > 0:
                prev_pvi = df.PVI.iloc[index - 1]
                prev_close = df.Close.iloc[index - 1]
                if df.vol_diff.iloc[index] > 0:
                    pvi = prev_pvi + (
                        (df.Close.iloc[index] - prev_close) / (prev_close * prev_pvi)
                    )
                else:
                    pvi = prev_pvi
            else:
                # Base PVI value is established (1000 is recommended)
                pvi = 1000
            df.PVI.iloc[index] = pvi
        df["PVI_EMA"] = df.PVI.ewm(ignore_na=False, com=self.rounds, adjust=True).mean()

        # Drop innecesary columns
        df.drop(["vol_diff"], axis=1, inplace=True)

        self.output = df
        return super().calculate(data, normalize)

    def calc_buy_signals(self):
        return self._calc_buy_signals(
            (self.output["PVI_EMA"].shift(1) > self.output["PVI"].shift(1))
            & (self.output["PVI_EMA"] <= self.output["PVI"])
        )

    def calc_sell_signals(self):
        return self._calc_sell_signals(
            (self.output["PVI_EMA"].shift(1) < self.output["PVI"].shift(1))
            & (self.output["PVI_EMA"] >= self.output["PVI"])
        )

    def plot(self):
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data["PVI_EMA"], color="gray", linewidth=1)
        plt.fill_between(
            data.index,
            data["PVI"],
            data["PVI_EMA"],
            where=data["PVI"] > data["PVI_EMA"],
            alpha=0.5,
            color="green",
        )
        plt.fill_between(
            data.index,
            data["PVI"],
            data["PVI_EMA"],
            where=data["PVI"] < data["PVI_EMA"],
            alpha=0.5,
            color="red",
        )
        plt.grid()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_pvi = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_pvi.iloc[-1]

        print(f"[PVI] Current pvi value: {new_signal.PVI}")
        print(f"[PVI] Current pvi_ema value: {new_signal.PVI_EMA}")

        signal = self.get_last_signal(as_enum)

        print(f"[PVI] Signal: {signal}")

        return signal
