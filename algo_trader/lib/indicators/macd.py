from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MACD(Indicator):
    def __init__(self, slow, fast, suavizado):
        self.slow = slow
        self.fast = fast
        self.suavizado = suavizado
        super().__init__("MACD")

    def calculate(self, data):
        df = pd.DataFrame(index=data.index)
        self.dates = data.index
        # Copy the 'Close' column from the original data to the DataFrame
        df["Close"] = data["Close"]

        # Calculate the fast exponential moving average
        df["ema_fast"] = df.Close.ewm(span=self.fast).mean()

        # Calculate the slow exponential moving average
        df["ema_slow"] = df.Close.ewm(span=self.slow).mean()

        # The difference between the fast and slow moving averages is another moving average called MACD
        df["macd"] = df.ema_fast - df.ema_slow

        # Smooth the MACD and call it the 'signal'
        df["signal"] = df.macd.ewm(span=self.suavizado).mean()

        # Finally, the point of interest is the difference between the MACD and the signal
        # It is particularly interesting when it crosses zero.
        df["histogram"] = df.macd - df.signal

        # Drop any NaN values and round the DataFrame to two decimal places
        df = df.dropna().round(2)

        # Rename the 'histogram' column with the indicator name for convenience (notation abuse)
        df[self.name] = df["histogram"]
        self.output = df[self.name]
        return self.output

    def calc_buy_signals(self):
        data = pd.DataFrame(self.output, index= self.dates)
        isUnderline = False
    
        buy_signals_list = []

        for i in range(0, len(data[self.name])):
            if (data[self.name].iloc[i] < 0):
                isUnderline = True
                buy_signals_list.append(0)
            else:
                buy_signals_list.append(1 if isUnderline == True else 0)
                isUnderline = False

        return buy_signals_list
    
    def calc_sell_signals(self):
        data = pd.DataFrame(self.output, index= self.dates)
        isOverline = False
        sell_signals_list = []

        for i in range(0, len(data[self.name])):
            if (data[self.name].iloc[i] > 0):
                isOverline = True
                sell_signals_list.append(0)
            else:
                sell_signals_list.append(1 if isOverline == True else 0)
                isOverline = False

        return sell_signals_list
    
    def plot(self):
        data = pd.DataFrame(self.output, index= self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(self.output)
        plt.grid()
        plt.axhline(0, linestyle='--', linewidth=1.5, color='black')
        plt.fill_between(data.index, self.output, 0, where=self.output>0, alpha=0.5, color='green')
        plt.fill_between(data.index, self.output, 0, where=self.output<0, alpha=0.5, color='red')
        plt.show()
