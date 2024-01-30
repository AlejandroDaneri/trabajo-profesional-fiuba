from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class NVI(Indicator):
    def __init__(self, rounds):
        self.rounds = rounds
        super().__init__("NVI")

    def calculate(self, data):
        # Disable SettingWithCopyWarning
        pd.options.mode.chained_assignment = None

        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        # Copy the 'Volume' column from the original data to the new DataFrame
        df["Volume"] = data["Volume"]

        # Initialize NVI column in zero
        df["NVI"] = 0.0

        for index in range(len(df)):
            if index > 0:
                prev_nvi = df.NVI.iloc[index-1]
                prev_close = df.Close.iloc[index-1]
                if df.Volume.iloc[index] < df.Volume.iloc[index-1]:
                    nvi = prev_nvi + (df.Close.iloc[index] - prev_close / prev_close * prev_nvi)
                else: 
                    nvi = prev_nvi
            else:
                nvi = 1000
            df.NVI.iloc[index] = nvi
        df["NVI_EMA"] = df.NVI.ewm(ignore_na=False, com=self.rounds, adjust=True).mean()
        
        self.output = df
        return self.output

    def calc_buy_signals(self):
        return np.where((self.output.shift(1) < self.buy_threshold) & (self.buy_threshold <= self.output), True, False)
    
    def calc_sell_signals(self):
        return np.where((self.output.shift(1) > self.sell_threshold) & (self.sell_threshold >= self.output), True, False)
    
    def plot(self):
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data["NVI"], color='green', linewidth=2)
        plt.plot(data["NVI_EMA"], color='red', linewidth=1)
        plt.grid()
        plt.show()

    def predict_signal(self, new_record):
        new_rsi = self.calculate(pd.concat([self.data, new_record]))
        sell_signal = self.calc_sell_signals()[-1]
        buy_signal = self.calc_buy_signals()[-1]

        new_signal = new_rsi.iloc[-1]

        print(f'[RSI] Current value: {new_signal}')
        print(f'[RSI] Sell Threshold: {self.sell_threshold}')
        print(f'[RSI] Buy Threshold: {self.buy_threshold}')

        if sell_signal == True:
            signal = Action.SELL
        elif buy_signal == True:
            signal = Action.BUY
        else:
            signal = Action.HOLD
        
        print(f'[RSI] Signal: {signal}')
        
        return signal
