from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class CandlesPatterns(Indicator):
    def __init__(self):
        super().__init__("CandlesPattern")

    def calculate(self, data, normalize=False):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        dojiCandleLength = 0.0002

        # Copy columns from the original data to the new DataFrame
        df["Close"] = data["Close"]
        df["Open"] = data["Open"]
        df["High"] = data["High"]
        df["Low"] = data["Low"]

        # Copy one day ago columns from the original data to the new DataFrame
        df["Close-1"] = df["Close"].shift(1).fillna(0)
        df["Open-1"] = df["Open"].shift(1).fillna(0)
        df["High-1"] = df["High"].shift(1).fillna(0)
        df["Low-1"] = df["Low"].shift(1).fillna(0)

        # Copy two day ago columns from the original data to the new DataFrame
        df["Close-2"] = df["Close"].shift(2).fillna(0)
        df["Open-2"] = df["Open"].shift(2).fillna(0)
        df["High-2"] = df["High"].shift(2).fillna(0)
        df["Low-2"] = df["Low"].shift(2).fillna(0)

        # Calculate the difference in volume between the current and previous rows
        df["Vol_diff"] = data["Volume"].diff()

        # Check if the candle shape is a bullish hammer
        df["Bullish_hammer"] = np.where(
            (df["Open-2"] > df["Close-2"]) &
            (abs(df["Open-1"] - df["Close-1"])*2 <= abs(df["Open-1"] - df["Low-1"])) &
            (abs(df["Open-1"] - df["Close-1"])*2 <= abs(df["Close-1"] - df["Low-1"])) &
            (
                (abs(df["High-1"] - df["Open-1"]) <= abs(df["Open-1"] - df["Close-1"])/2) |
                (abs(df["High-1"] - df["Close-1"]) <= abs(df["Open-1"] - df["Close-1"])/2)
            ) &
            (df["Open"] < df["Close"]),
            True, False)

        # Check if the candle shape is a bullish engulfing
        df["Bullish_engulfing"] = np.where(
            (df["Open-2"] > df["Close-2"]) &
            (df["Open-1"] > df["Close-1"]) &
            (df["Open"] < df["Close"]) &
            (abs(df["Open"] - df["Close"]) > abs(df["Open-1"] - df["Close-1"])) &
            (df["Vol_diff"] > 0),
            True, False)

        # Check if the candle shape is a morning star
        df["Morning_star"] = np.where(
            (df["Open-2"] > df["Close-2"]) &
            ((abs(df["Open-1"]/df["Close-1"]) - 1) <= dojiCandleLength) &
            (df["Open"] < df["Close"]) &
            (abs(df["Open"] - df["Close"]) > abs(df["Open-2"] - df["Close-2"])/2),
            True, False)
        
        df["Bullish_signal"] = np.where(
            df["Bullish_hammer"] | df["Bullish_engulfing"] | df["Morning_star"],
            True, False
        )

        # Check if the candle shape is a shooting star
        df["Shooting_star"] = np.where(
            (df["Open-2"] < df["Close-2"]) &
            (abs(df["Open-1"] - df["Close-1"])*2 <= abs(df["Open-1"] - df["High-1"])) &
            (abs(df["Open-1"] - df["Close-1"])*2 <= abs(df["Close-1"] - df["High-1"])) &
            (
                (abs(df["Low-1"] - df["Open-1"]) <= abs(df["Open-1"] - df["Close-1"])/2) |
                (abs(df["Low-1"] - df["Close-1"]) <= abs(df["Open-1"] - df["Close-1"])/2)
            ) &
            (df["Open"] > df["Close"]),
            True, False)

        # Check if the candle shape is a bearish engulfing
        df["Bearish_engulfing"] = np.where(
            (df["Open-2"] < df["Close-2"]) &
            (df["Open-1"] < df["Close-1"]) &
            (df["Open"] > df["Close"]) &
            (abs(df["Open"] - df["Close"]) > abs(df["Open-1"] - df["Close-1"])) &
            (df["Vol_diff"] > 0),
            True, False)

        # Check if the candle shape is a evening star
        df["Evening_star"] = np.where(
            (df["Open-2"] < df["Close-2"]) &
            ((abs(df["Open-1"]/df["Close-1"]) - 1) <= dojiCandleLength) &
            (df["Open"] > df["Close"]) &
            (abs(df["Open"] - df["Close"]) > abs(df["Open-2"] - df["Close-2"])/2),
            True, False)
        
        # Check if the candle shape is a hanging man
        df["Hanging_man"] = np.where(
            (df["Open-2"] < df["Close-2"]) &
            (df["Open-1"] > df["Close-1"]) &
            (abs(df["Open-1"] - df["Close-1"])*2 <= abs(df["Close-1"] - df["Low-1"])) &
            (abs(df["High-1"] - df["Open-1"]) <= abs(df["Open-1"] - df["Close-1"])/2) &
            (df["Open"] > df["Close"]),
            True, False)
        
        df["Bearish_signal"] = np.where(
            df["Shooting_star"] | df["Bearish_engulfing"] | df["Evening_star"] | df["Hanging_man"],
            True, False
        )

        self.df_output = df[["Open", "Close", "High", "Low", "Bullish_signal", "Bearish_signal"]]
        return self.df_output

    def calc_buy_signals(self):
        return self._calc_buy_signals(
            self.df_output["Bullish_signal"]
        )

    def calc_sell_signals(self):
        return self._calc_sell_signals(
            self.df_output["Bearish_signal"]
        )

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        print(f"[Candles Patterns] Current Bullish Signal: {new_signal.Bullish_signal}")
        print(f"[Candles Patterns] Current Bearish Signal: {new_signal.Bearish_signal}")

        signal = self.get_last_signal(as_enum)

        print(f"[Candles Patterns] Signal: {signal}")

        return signal