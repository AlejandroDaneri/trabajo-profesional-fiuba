from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class DMI(Indicator):
    def __init__(self, rounds, adx_threshold):
        self.rounds = rounds
        self.adx_threshold = adx_threshold
        super().__init__("DMI")

    def calculate(self, data):
        # Calculate ATR (Average True Range)
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates= data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        df["HighLow"] = data["High"] - data["Low"]
        df["HighClose"] = abs(data["High"] - data["Close"].shift(1))
        df["LowClose"] = abs(data["Low"] - data["Close"].shift(1))

        df["TrueRange"] = df[["HighLow", "HighClose", "LowClose"]].max(axis=1, skipna=False)
        df["ATR"] = df["TrueRange"].ewm(span=self.rounds, min_periods=self.rounds).mean()

        # Drop innecesary columns
        df.drop(["HighLow", "HighClose", "LowClose", "TrueRange"], axis=1, inplace=True)

        # Calculate DMI and ADX
        df["UpMove"] = data["High"] - data["High"].shift(1)
        df["DownMove"] = data["Low"].shift(1) - data["Low"]
        df["+dm"] = np.where((df["UpMove"] > df["DownMove"]) & (df["UpMove"] > 0), df["UpMove"], 0)
        df["-dm"] = np.where((df["DownMove"] > df["UpMove"]) & (df["DownMove"] > 0), df["DownMove"], 0)
        df["+di"] = 100 * (df["+dm"]/df["ATR"]).ewm(alpha=1/self.rounds, min_periods=self.rounds).mean()
        df["-di"] = 100 * (df["-dm"]/df["ATR"]).ewm(alpha=1/self.rounds, min_periods=self.rounds).mean()
        df["ADX"] = 100 * abs((df["+di"] - df["-di"])/(df["+di"] + df["-di"])).ewm(alpha=1/self.rounds, min_periods=self.rounds).mean()

        # Drop innecesary columns
        df.drop(["UpMove", "DownMove", "+dm", "-dm", "ATR"], axis=1, inplace=True)

        self.output = df
        return self.output

    def calc_buy_signals(self):
        return np.where((self.output["-di"].shift(1) > self.output["+di"].shift(1)) & 
                        (self.output["-di"] <= self.output["+di"]) &
                        (self.adx_threshold <= self.output["ADX"]), True, False)
    
    def calc_sell_signals(self):
        return np.where((self.output["-di"].shift(1) < self.output["+di"].shift(1)) & 
                        (self.output["-di"] >= self.output["+di"]) &
                        (self.adx_threshold <= self.output["ADX"]), True, False)
    
    def plot(self):
        data = pd.DataFrame(self.output, index= self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data["+di"], color='green', linewidth=1)
        plt.plot(data["-di"], color='red', linewidth=1)
        plt.plot(data["ADX"], color='blue', linewidth=2)
        plt.grid()
        # Threshold
        plt.axhline(self.adx_threshold, linestyle='--', linewidth=1.5, color='gray')
        plt.show()

    def predict_signal(self, new_record):
        new_dmi = self.calculate(pd.concat([self.data, new_record]))
        sell_signal = self.calc_sell_signals()[-1]
        buy_signal = self.calc_buy_signals()[-1]

        new_signal = new_dmi.iloc[-1]

        print(f'[DMI] Current value:\n{new_signal}')
        print(f'[DMI] ADX Threshold: {self.adx_threshold}')

        if sell_signal == True:
            signal = Action.SELL
        elif buy_signal == True:
            signal = Action.BUY
        else:
            signal = Action.HOLD
        
        print(f'[DMI] Signal: {signal}')
        
        return signal
