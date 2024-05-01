from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class SAR(Indicator):
    def __init__(self, initial_af: float = 0.02, max_af: float = 0.20, af_increment: float = 0.02):
        self.initial_af = initial_af
        self.max_af = max_af
        self.af_increment = af_increment
        super().__init__("SAR")

    def calculate(self, data, normalize=False):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Disable SettingWithCopyWarning
        pd.options.mode.chained_assignment = None

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        # Copy the 'High' column from the original data to the new DataFrame
        df["High"] = data["High"]

        # Copy the 'Low' column from the original data to the new DataFrame
        df["Low"] = data["Low"]

        # Create columns for SAR, AF (Aceleration Factor), and EP (Extreme Point)
        df["SAR"] = 0.0
        df["AF"] = 0.0
        df["EP"] = 0.0

        # Determine the starting trend (True for uptrend, False for downtrend)
        uptrend = df["Close"].iloc[0] < df["Close"].iloc[1]

        # Initialize first row values
        df["SAR"].iloc[0] = df["Low"].iloc[0] if uptrend else df["High"].iloc[0]
        df["AF"].iloc[0] = self.initial_af
        df["EP"].iloc[0] = df["High"].iloc[0] if uptrend else df["Low"].iloc[0]

        for i in range(1, len(df)):
            prev_sar = df["SAR"].iloc[i - 1]
            prev_af = df["AF"].iloc[i - 1]
            prev_ep = df["EP"].iloc[i - 1]

            # Calculate current SAR
            df["SAR"].iloc[i] = prev_sar + prev_af * (prev_ep - prev_sar)

            # Check for trend reversal
            if (uptrend and df["SAR"].iloc[i] > df["Low"].iloc[i]) or (
                not uptrend and df["SAR"].iloc[i] < df["High"].iloc[i]
            ):
                # Reverse the trend
                uptrend = not uptrend
                # Set SAR to the EP of the previous trend
                df["SAR"].iloc[i] = prev_ep
                # Reset AF
                df["AF"].iloc[i] = self.initial_af
                # Set EP to current's high/low
                df["EP"].iloc[i] = df["High"].iloc[i] if uptrend else df["Low"].iloc[i]
            else:
                # Update AF and EP if a new high/low is made
                if (uptrend and df["High"].iloc[i] > prev_ep) or (
                    not uptrend and df["Low"].iloc[i] < prev_ep
                ):
                    # Increment AF, cap at max_af
                    df["AF"].iloc[i] = min(self.max_af, prev_af + self.af_increment)
                    # Update EP to current's high/low
                    df["EP"].iloc[i] = (
                        df["High"].iloc[i] if uptrend else df["Low"].iloc[i]
                    )
                else:
                    # Carry over AF
                    df["AF"].iloc[i] = prev_af
                    # Carry over EP
                    df["EP"].iloc[i] = prev_ep

        # Drop innecesary columns
        df.drop(["AF", "EP"], axis=1, inplace=True)

        self.df_output = df
        return self.df_output

    def calc_buy_signals(self):
        return self._calc_buy_signals(
            (self.df_output.High.shift(1) <= self.df_output.SAR.shift(1))
            & (self.df_output.SAR < self.df_output.High)
        )

    def calc_sell_signals(self):
        return self._calc_sell_signals(
            (self.df_output.SAR.shift(1) <= self.df_output.Low.shift(1).fillna(0))
            & (self.df_output.Low < self.df_output.SAR)
        )

    def plot(self):
        data = pd.DataFrame(self.df_output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(
            data.index, data.SAR, color="blue", marker="o", linewidth=0, markersize=1
        )
        plt.grid()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        print(f"[SAR] Current SAR value: {new_signal.SAR}")
        print(f"[SAR] Current High value: {new_signal.High}")
        print(f"[SAR] Current Low value: {new_signal.Low}")

        signal = self.get_last_signal(as_enum)

        print(f"[SAR] Signal: {signal}")

        return signal