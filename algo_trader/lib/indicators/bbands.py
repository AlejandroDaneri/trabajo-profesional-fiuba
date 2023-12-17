from lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class BBANDS(Indicator):
  def __init__(self, rounds, factor):
        # Moving Average periods 
        self.rounds = rounds
        # Factor to shift the bands
        self.factor = factor
        super().__init__("BBANDS")

  def calculate(self, data):
    df = pd.DataFrame(index=data.index)
    self.dates= data.index

    # Copy the 'Close' column from the original data to the DataFrame
    df["Close"] = data["Close"]

    # Calculate the average of the last n rounds of Close
    df["MidBand"] = data["Close"].rolling(self.rounds).mean()

    # Calculate the Standard Deviation of the last n rounds of Close
    df["Std"] = data["Close"].rolling(self.rounds).std()

    # Calculate the upper band
    df["UpperBand"] = df["MidBand"] + df["Std"]*self.factor

    # Calculate the lower band
    df["LowerBand"] = df["MidBand"] - df["Std"]*self.factor

    self.df_output = df
    return self.df_output
  
  def calc_buy_signals(self):
    data = pd.DataFrame(self.output, index= self.dates)
    isOverbought = False
  
    buy_signals_list = []

    for i in range(0, len(data[self.name])):
      if (data[self.name].iloc[i] < 30):
        isOverbought = True
        buy_signals_list.append(0)
      else:
        buy_signals_list.append(1 if isOverbought == True else 0)
        isOverbought = False

    return buy_signals_list
  
  def calc_sell_signals(self):
    data = pd.DataFrame(self.output, index= self.dates)
    isOversold = False
    sell_signals_list = []

    for i in range(0, len(data[self.name])):
      if (data[self.name].iloc[i] > 70):
        isOversold = True
        sell_signals_list.append(0)
      else:
        sell_signals_list.append(1 if isOversold == True else 0)
        isOversold = False

    return sell_signals_list
  
  def plot(self):
    data = self.df_output
    
    fig = plt.figure()
    fig.set_size_inches(16, 8)
    plt.plot(data.index, data.Close)
    plt.plot(data.index, data.MidBand, linewidth = 0.5, linestyle = "dashed")
    plt.plot(data.index, data.UpperBand, linewidth = 0.5, color = "#033660")
    plt.plot(data.index, data.LowerBand, linewidth = 0.5, color = "#033660")
    plt.grid()
    plt.show()
