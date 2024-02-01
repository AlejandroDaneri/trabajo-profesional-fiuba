from lib.indicators.indicator import Indicator
from lib.actions import Action
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from algo_trader.lib.indicators.nvi import NVI
from algo_trader.lib.indicators.pvi import PVI
from algo_trader.lib.indicators.mfi import MFI

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
        df["TP"] = (data['Open'] + data['High'] + data['Low'] + data['Close']) / 4

        # Calculate the pvi
        nvi = PVI(255)
        df["PVI"] = nvi.calculate(data).PVI
        df["PVI_M"] = df["PVI"].ewm(span=15, adjust=False).mean()
        df["PVI_MAX"] = df["PVI_M"].rolling(window=90).max()
        df["PVI_MIN"] = df["PVI_M"].rolling(window=90).min()
        df["OSCP"] = (df["PVI"] - df["PVI_M"]) * 100 / (df["PVI_MAX"] - df["PVI_MIN"])

        # Calculate the nvi
        nvi = NVI(255)
        df["NVI"] = nvi.calculate(data).NVI
        df["NVI_M"] = df["NVI"].ewm(span=15, adjust=False).mean()
        df["NVI_MAX"] = df["NVI_M"].rolling(window=90).max()
        df["NVI_MIN"] = df["NVI_M"].rolling(window=90).min()

        # Calculate the mfi
        mfi = MFI(20, 80, 14)
        df["MFI"] = mfi.calculate(data)

        # Calculate the bollinger bands
        df["BOLL_BASIS"] = df["TP"].rolling(25).mean()
        df["Std"] = 2.0 * df["TP"].rolling(25).std()
        df["UpperBand"] = df["BOLL_BASIS"] + df["Std"]
        df["LowerBand"] = df["BOLL_BASIS"] - df["Std"]
        df["OB1"] = (df["UpperBand"] + df["LowerBand"]) / 2.0
        df["OB2"] = df["UpperBand"] - df["LowerBand"]
        df["BOLL_OSC"] = ((df["TP"] - df["OB1"]) / df["OB2"]) * 100

        # Calculate the rsi based in TP value
        df["TP_diff"] = df["TP"].diff()
        df["TP_win"] = np.where(df["TP_diff"] > 0, df["TP_diff"], 0)
        df["TP_loss"] = np.where(df["TP_diff"] < 0, abs(df["TP_diff"]), 0)
        df["TP_EMA_win"] = df["TP_win"].ewm(alpha=1 / 14).mean()
        df["TP_EMA_loss"] = df["TP_loss"].ewm(alpha=1 / 14).mean()
        df["TP_RS"] = df["TP_EMA_win"] / df["TP_EMA_loss"]
        df["RSI"] = 100 - (100 / (1 + df["TP_RS"]))

        # Calculate the Stochastic
        df["LL"] = data["Low"].rolling(window=21).min()
        df["HH"] = data["High"].rolling(window=21).max()
        df["K"] = 100 * (df["TP"] - df["LL"]) / (df["HH"] - df["LL"])
        df["STOCH"] = df["K"].rolling(3).mean()

        # Calculate values
        df["BLUE_INDEX"] = (df["NVI"] - df["NVI_M"]) * 100 / (df["NVI_MAX"] - df["NVI_MIN"])
        df["BROWN_INDEX"] = (df["RSI"] + df["MFI"] + df["BOLL_OSC"] + (df["STOCH"] / 3)) / 2
        df["GREEN_INDEX"] = (df["BROWN_INDEX"] + df["OSCP"])
        df["AVG_INDEX"] = df["BROWN_INDEX"].ewm(span=15, adjust=False).mean()

        self.output = df
        return self.output

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
        plt.fill_between(data.index, data["GREEN_INDEX"], 0, where=data["GREEN_INDEX"], alpha=0.5, color='green')
        plt.fill_between(data.index, data["BROWN_INDEX"], 0, where=data["BROWN_INDEX"], alpha=0.5, color='yellow')
        plt.fill_between(data.index, data["BLUE_INDEX"], 0, where=data["BLUE_INDEX"], alpha=0.5, color='blue')
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