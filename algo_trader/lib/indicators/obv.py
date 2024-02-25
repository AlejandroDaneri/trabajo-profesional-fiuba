from lib.actions import Action
from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class OBV(Indicator):
    def __init__(self, rounds):
        self.rounds = rounds
        super().__init__("OBV")

    def calculate(self, data):
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index

        # Copy the 'Close' column from the original data to the new DataFrame
        df["Close"] = data["Close"]

        # Calculate the balance volume
        change = data.Close.diff()
        df["OBV"] = np.cumsum(np.where(change > 0, data.Volume, np.where(change < 0, -data.Volume, 0)))

        # Calculate the EMA from balance volume
        df["OBV_EMA"] = df["OBV"].ewm(span=self.rounds, adjust=False).mean()

        self.df_output = df
        return self.df_output

    def calc_buy_signals(self):
        return np.where(
            (self.df_output.OBV.shift(1) < self.df_output.OBV_EMA.shift(1)) & 
            (self.df_output.OBV_EMA <= self.df_output.OBV), True, False)

    def calc_sell_signals(self):
        return np.where(
            (self.df_output.OBV_EMA.shift(1) < self.df_output.OBV.shift(1).fillna(0)) & 
            (self.df_output.OBV <= self.df_output.OBV_EMA), True, False)

    def plot(self):
        data = pd.DataFrame(self.df_output, index=self.dates)
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data.OBV, color='blue', linewidth=1)
        plt.plot(data.OBV_EMA, color='green', linewidth=0.5)
        plt.show()

    def predict_signal(self, new_record):
        # Calculate OBV for the updated DataFrame
        new_obv = self.calculate(pd.concat([self.data, new_record]))
        sell_signal = self.calc_sell_signals()[-1]
        buy_signal = self.calc_buy_signals()[-1]

        # Extract the value of OBV for the new record
        new_signal = new_obv.iloc[-1]

        print(f'[OBV] Current OBV value: {new_signal.OBV}')
        print(f'[OBV] Current OBV_EMA value: {new_signal.OBV_EMA}')

        # Trading decisions based on OBV signals
        if sell_signal == True:
            signal = Action.SELL
        elif buy_signal == True:
            signal = Action.BUY
        else:
            signal = Action.HOLD
        
        print(f'[OBV] Signal: {signal}')
        
        return signal
