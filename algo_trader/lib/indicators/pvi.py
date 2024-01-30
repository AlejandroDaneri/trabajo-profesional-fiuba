from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class PVI(Indicator):
    def __init__(self, rounds):
        self.rounds = rounds
        super().__init__("PVI")

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

        # Initialize PVI column in zero
        df["PVI"] = 0.0

        # Calculate each PVI value based on its previous PVI value
        for index in range(len(df)):
            if index > 0:
                prev_pvi = df.PVI.iloc[index-1]
                prev_close = df.Close.iloc[index-1]
                if df.Volume.iloc[index] < df.Volume.iloc[index-1]:
                    pvi = prev_pvi + (df.Close.iloc[index] - prev_close / prev_close * prev_pvi)
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
        return self.output

    def calc_buy_signals(self):
        return np.where((self.output["PVI_EMA"].shift(1) > self.output["PVI"].shift(1)) & 
                        (self.output["PVI_EMA"] <= self.output["PVI"]), True, False)
    
    def calc_sell_signals(self):
        return np.where((self.output["PVI_EMA"].shift(1) < self.output["PVI"].shift(1)) & 
                        (self.output["PVI_EMA"] >= self.output["PVI"]), True, False)
    
    def plot(self):
        data = pd.DataFrame(self.output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data["NVI"], color='green', linewidth=2)
        plt.plot(data["NVI_EMA"], color='red', linewidth=1)
        plt.grid()
        plt.show()

    def predict_signal(self, new_record):
        new_nvi = self.calculate(pd.concat([self.data, new_record]))
        sell_signal = self.calc_sell_signals()[-1]
        buy_signal = self.calc_buy_signals()[-1]

        new_signal = new_nvi.iloc[-1]

        print(f'[NVI] Current nvi value: {new_signal.NVI}')
        print(f'[NVI] Current nvi_ema value: {new_signal.NVI_EMA}')

        if sell_signal == True:
            signal = Action.SELL
        elif buy_signal == True:
            signal = Action.BUY
        else:
            signal = Action.HOLD
        
        print(f'[NVI] Signal: {signal}')
        
        return signal
