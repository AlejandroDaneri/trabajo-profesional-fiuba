from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class RSI(Indicator):
    def __init__(self, buy_threshold, sell_threshold, rounds):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.rounds = rounds
        super().__init__("RSI")

    def calculate(self, data):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        # Calculate the difference in closing prices between the current and previous rows
        df["diff"] = df.Close.diff()

        # If the difference is greater than 0, set the 'win' column to the difference; otherwise, set it to 0
        df["win"] = np.where(df["diff"] > 0, df["diff"], 0)

        # If the difference is less than 0, set the 'loss' column to the absolute difference; otherwise, set it to 0
        df["loss"] = np.where(df["diff"] < 0, abs(df["diff"]), 0)

        # Calculate the exponential moving average of the 'win' column
        df["EMA_win"] = df.win.ewm(alpha=1 / self.rounds).mean()

        # Calculate the exponential moving average of the 'loss' column
        df["EMA_loss"] = df.loss.ewm(alpha=1 / self.rounds).mean()

        # Calculate the ratio between the exponential moving averages ('RS' column)
        df["RS"] = df.EMA_win / df.EMA_loss
        df[self.name] = 100 - (100 / (1 + df["RS"]))  # TODO: Check vs alphavantage API

        # Calculate the final Relative Strength Index (RSI) using the calculated RS
        self.output = df[self.name]

        return self.output

    def calc_buy_signals(self):
        return np.where((self.output.shift(1) < self.buy_threshold) & (self.buy_threshold <= self.output), True, False)
    
    def calc_sell_signals(self):
        return np.where((self.output.shift(1) > self.sell_threshold) & (self.sell_threshold >= self.output), True, False)
    
    def plot(self):
        data = pd.DataFrame(self.output, index= self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data[self.name], color='orange', linewidth=2)
        plt.grid()
        # Oversold
        plt.axhline(30, linestyle='--', linewidth=1.5, color='green')
        # Overbought
        plt.axhline(70, linestyle='--', linewidth=1.5, color='red')
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
