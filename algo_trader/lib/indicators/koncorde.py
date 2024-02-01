from lib.indicators.indicator import Indicator
from lib.actions import Action
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from algo_trader.lib.indicators.nvi import NVI
from algo_trader.lib.indicators.pvi import PVI
from algo_trader.lib.indicators.mfi import MFI
from algo_trader.lib.indicators.rsi import RSI

class KONCORDE(Indicator):
    def __init__(self, rounds):
        self.rounds = rounds
        super().__init__("KONCORDE")

    def calculate(self, data):
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the DataFrame
        df["Close"] = data["Close"]

        # Calculate the typical price, its is the average of the maximum, minimum, open and close price
        typical_price = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4

        # Calculate Stochastic indicator of typical price
        storch = self.calc_stoch(typical_price, data, 21, 3) / 3

        # Calculate the mfi
        mfi = MFI(20, 80, 14)
        mfi_values = mfi.calculate(data)

        # Calculate the bollinger bands
        df["BOLL_BASIS"] = typical_price.rolling(25).mean()
        df["Std"] = 2.0 * typical_price.rolling(25).std()
        df["UpperBand"] = df["BOLL_BASIS"] + df["Std"]
        df["LowerBand"] = df["BOLL_BASIS"] - df["Std"]
        df["OB1"] = (df["UpperBand"] + df["LowerBand"]) / 2.0
        df["OB2"] = df["UpperBand"] - df["LowerBand"]
        df["BOLL_OSC"] = ((typical_price - df["OB1"]) / df["OB2"]) * 100

        # Calculate the rsi based in TP value
        rsi_values = self.calc_rsi(typical_price, 14)

        # Calculate values
        df["BIG_HANDS"] = self.calc_nvi(data, 15)
        df["BROWN_INDEX"] = (rsi_values + mfi_values + df["BOLL_OSC"] + (storch / 3)) / 2
        df["SMALL_HANDS"] = (df["BROWN_INDEX"] + self.calc_pvi(data, 15))
        df["AVG_INDEX"] = df["BROWN_INDEX"].ewm(span=15, adjust=False).mean()

        self.output = df
        return self.output

    # Calculate the NVI to detect large investments (blue graphic)
    def calc_nvi(self, data, rounds):
        nvi = NVI(255)
        nvi_values = nvi.calculate(data).NVI
        return self.calc_volume_index(nvi_values, rounds, 90)
    
    # Calculate the PVI to detect small investments (green graphic)
    def calc_pvi(self, data, rounds):
        pvi = PVI(255)
        pvi_values = pvi.calculate(data).PVI
        return self.calc_volume_index(pvi_values, rounds, 90)

    def calc_volume_index(self, vi, mean_rounds, length):
        vi_mean = vi.ewm(span=mean_rounds, adjust=False).mean()
        vi_max = vi_mean.rolling(window=length).max()
        vi_min = vi_mean.rolling(window=length).min()
        return (vi - vi_mean) * 100 / (vi_max - vi_min)
    
    # Calculate Stochastic indicator
    def calc_stoch(self, src, data, length, smoothFastD):
        lowestLow = data['Low'].rolling(window=length).min()
        highestHigh = data['High'].rolling(window=length).max()
        currentValue = 100 * (src - lowestLow) / (highestHigh - lowestLow)
        return currentValue.rolling(smoothFastD).mean()
    
    # Calculate RSI indicator
    def calc_rsi(self, src, rounds):
        rsi = RSI(30, 70, rounds)
        df = pd.DataFrame(src, columns = ['Close'])
        return rsi.calculate(df)

    def calc_buy_signals(self):
        return np.where((self.output.BROWN_INDEX.shift(1) < self.output.AVG_INDEX.shift(1)) 
                        & (self.output.AVG_INDEX <= self.output.BROWN_INDEX), True, False)
    
    def calc_sell_signals(self):
        return np.where((self.output.BROWN_INDEX.shift(1) > self.output.AVG_INDEX.shift(1)) 
                        & (self.output.AVG_INDEX >= self.output.BROWN_INDEX), True, False)
    
    def plot(self):
        data = pd.DataFrame(self.output, index= self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.axhline(0, linestyle='--', linewidth=1.5, color='black')
        plt.fill_between(data.index, data["SMALL_HANDS"], 0, where=data["SMALL_HANDS"], alpha=0.5, color='green')
        plt.fill_between(data.index, data["BROWN_INDEX"], 0, where=data["BROWN_INDEX"], alpha=0.5, color='yellow')
        plt.fill_between(data.index, data["BIG_HANDS"], 0, where=data["BIG_HANDS"], alpha=0.5, color='blue')
        plt.plot(data.index, data["AVG_INDEX"], color='red', linewidth=1)
        plt.grid()
        plt.show()

    def predict_signal(self, new_record):
        new_koncorde_value = self.calculate(pd.concat([self.data, new_record]))
        sell_signal = self.calc_sell_signals()[-1]
        buy_signal = self.calc_buy_signals()[-1]

        if sell_signal == True:
            signal = Action.SELL
        elif buy_signal == True:
            signal = Action.BUY
        else:
            signal = Action.HOLD

        print(f'[KONCORDE] Signal: {signal}')
        
        return signal