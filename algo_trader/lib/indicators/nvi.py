from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class NVI(Indicator):
    def __init__(self, rounds):
        self.rounds = rounds
        super().__init__("NVI")

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

        # Initialize NVI column in zero
        df["NVI"] = 0.0

        # Calculate each NVI value based on its previous NVI value
        for index in range(len(df)):
            if index > 0:
                prev_nvi = df.NVI.iloc[index - 1]
                prev_close = df.Close.iloc[index - 1]
                if df.vol_diff.iloc[index] < 0:
                    nvi = prev_nvi + (
                        (df.Close.iloc[index] - prev_close) / (prev_close * prev_nvi)
                    )
                else:
                    nvi = prev_nvi
            else:
                # Base NVI value is established (1000 is recommended)
                nvi = 1000
            df.NVI.iloc[index] = nvi
        df["NVI_EMA"] = df.NVI.ewm(ignore_na=False, com=self.rounds, adjust=True).mean()

        # Drop innecesary columns
        df.drop(["vol_diff"], axis=1, inplace=True)

        self.output = df
        return super().calculate(data, normalize)

    def calc_buy_signals(self):
        return np.where(
            (self.output["NVI_EMA"].shift(1) > self.output["NVI"].shift(1))
            & (self.output["NVI_EMA"] <= self.output["NVI"]),
            True,
            False,
        )

    def calc_sell_signals(self):
        return np.where(
            (self.output["NVI_EMA"].shift(1) < self.output["NVI"].shift(1))
            & (self.output["NVI_EMA"] >= self.output["NVI"]),
            True,
            False,
        )

    def plot(self):
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data["NVI_EMA"], color="gray", linewidth=1)
        plt.fill_between(
            data.index,
            data["NVI"],
            data["NVI_EMA"],
            where=data["NVI"] > data["NVI_EMA"],
            alpha=0.5,
            color="green",
        )
        plt.fill_between(
            data.index,
            data["NVI"],
            data["NVI_EMA"],
            where=data["NVI"] < data["NVI_EMA"],
            alpha=0.5,
            color="red",
        )
        plt.grid()
        plt.show()

    def predict_signal(self, new_record):
        new_nvi = self.calculate(pd.concat([self.data, new_record]))
        sell_signal = self.calc_sell_signals()[-1]
        buy_signal = self.calc_buy_signals()[-1]

        new_signal = new_nvi.iloc[-1]

        print(f"[NVI] Current nvi value: {new_signal.NVI}")
        print(f"[NVI] Current nvi_ema value: {new_signal.NVI_EMA}")

        if sell_signal == True:
            signal = Action.SELL
        elif buy_signal == True:
            signal = Action.BUY
        else:
            signal = Action.HOLD

        print(f"[NVI] Signal: {signal}")

        return signal
