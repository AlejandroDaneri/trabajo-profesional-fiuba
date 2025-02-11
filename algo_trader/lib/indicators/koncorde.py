from lib.indicators.indicator import Indicator
from lib.actions import Action
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lib.indicators.nvi import NVI
from lib.indicators.pvi import PVI
from lib.indicators.mfi import MFI
from lib.indicators.rsi import RSI
from lib.indicators.bbands import BBANDS
from lib.indicators.stochastic import Stochastic


class KONCORDE(Indicator):
    def __init__(self, rounds: int, rsi_mfi_length: int = 14, bbands_length: int = 25, bbands_factor: float = 2.0, stoch_length: int = 21):
        self.rounds = rounds
        self.rsi_mfi_length = rsi_mfi_length
        self.bbands_length = bbands_length
        self.bbands_factor = bbands_factor
        self.stoch_length = stoch_length
        super().__init__("KONCORDE")

    def calculate(self, data, normalize=False):
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the DataFrame
        df["Close"] = data["Close"]

        # Calculate the typical price, its is the average of the maximum, minimum, open and close price
        typical_price = (
            data["Open"].fillna(0)
            + data["High"].fillna(0)
            + data["Low"].fillna(0)
            + data["Close"].fillna(0)
        ) / 4

        # Calculate Stochastic indicator of typical price
        stoch = self.calc_stoch(typical_price, data, self.stoch_length)

        # Calculate the mfi
        mfi = MFI(
            0, 0, self.rsi_mfi_length
        )  # buy_threshold and sell_threshold parameters is not used here
        mfi_values = mfi.calculate(data)

        # Calculate the rsi based in TP value
        rsi_values = self.calc_rsi(typical_price, self.rsi_mfi_length)

        # Calculate Bollinger Bands oscilator
        boll_osc = self.calc_bbands_osc(
            typical_price, self.bbands_length, self.bbands_factor
        )

        # Calculate values
        df["BIG_HANDS"] = self.calc_nvi(data, self.rounds)
        df["TREND"] = (rsi_values + mfi_values + boll_osc + (stoch / 3)) / 2
        df["SMALL_HANDS"] = df["TREND"] + self.calc_pvi(data, self.rounds)
        df["TREND_AVG"] = df["TREND"].ewm(span=self.rounds, adjust=False).mean()

        self.output = df
        return super().calculate(data, normalize)

    # Calculate the NVI to detect large investments (blue graphic)
    def calc_nvi(self, data, rounds):
        nvi = NVI(0)  # rounds parameter is not used here
        nvi_values = nvi.calculate(data).NVI
        return self.calc_volume_index(nvi_values, rounds, 90)

    # Calculate the PVI to detect small investments (green graphic)
    def calc_pvi(self, data, rounds):
        pvi = PVI(0)  # rounds parameter is not used here
        pvi_values = pvi.calculate(data).PVI
        return self.calc_volume_index(pvi_values, rounds, 90)

    def calc_volume_index(self, vi, avg_rounds, length):
        vi_avg = vi.ewm(span=avg_rounds, adjust=False).mean()
        vi_max = vi_avg.rolling(window=length).max()
        vi_min = vi_avg.rolling(window=length).min()
        return (vi - vi_avg) * 100 / (vi_max - vi_min)

    # Calculate Stochastic indicator
    def calc_stoch(self, src, data, rounds):
        stoch = Stochastic(
            0, 0, rounds
        )  # buy_threshold and sell_threshold parameters is not used here
        df = pd.DataFrame(src, columns=["Close"])
        df["High"] = data["High"]
        df["Low"] = data["Low"]
        return stoch.calculate(df)["%D"]

    # Calculate RSI indicator
    def calc_rsi(self, src, rounds):
        rsi = RSI(
            0, 0, rounds
        )  # buy_threshold and sell_threshold parameters is not used here
        df = pd.DataFrame(src, columns=["Close"])
        return rsi.calculate(df)

    # Calculate Bollinger Bands oscilator
    def calc_bbands_osc(self, src, rounds, factor):
        bbands = BBANDS(rounds, factor)
        df = pd.DataFrame(src, columns=["Close"])
        df_bbands = bbands.calculate(df)
        ob1 = (df_bbands["UpperBand"] + df_bbands["LowerBand"]) / factor
        ob2 = df_bbands["UpperBand"] - df_bbands["LowerBand"]
        return ((src - ob1) / ob2) * 100

    def calc_buy_signals(self):
        return self._calc_buy_signals(
            (self.output.TREND.shift(1) < self.output.TREND_AVG.shift(1))
            & (self.output.TREND_AVG <= self.output.TREND)
        )

    def calc_sell_signals(self):
        return self._calc_sell_signals(
            (self.output.TREND.shift(1) > self.output.TREND_AVG.shift(1))
            & (self.output.TREND_AVG >= self.output.TREND)
        )

    def plot(self):
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.axhline(0, linestyle="--", linewidth=1.5, color="black")
        plt.fill_between(
            data.index,
            data["SMALL_HANDS"],
            0,
            where=data["SMALL_HANDS"],
            alpha=0.5,
            color="green",
        )
        plt.fill_between(
            data.index, data["TREND"], 0, where=data["TREND"], alpha=0.5, color="yellow"
        )
        plt.fill_between(
            data.index,
            data["BIG_HANDS"],
            0,
            where=data["BIG_HANDS"],
            alpha=0.5,
            color="blue",
        )
        plt.plot(data.index, data["TREND_AVG"], color="red", linewidth=1)
        plt.grid()
        plt.show()

    def predict_signal(self, new_record, as_enum=True):
        new_koncorde_value = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_koncorde_value.iloc[-1]

        print(f"[KONCORDE] Small hands value: {new_signal.SMALL_HANDS}")
        print(f"[KONCORDE] Big hands value: {new_signal.BIG_HANDS}")
        print(f"[KONCORDE] Trend value: {new_signal.TREND}")
        print(f"[KONCORDE] Trend avg value: {new_signal.TREND_AVG}")

        signal = self.get_last_signal(as_enum)

        print(f"[KONCORDE] Signal: {signal}")

        return signal