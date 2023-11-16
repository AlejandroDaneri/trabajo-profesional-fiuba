from indicators.indicator import Indicator
import numpy as np
import pandas as pd

class Sigma(Indicator):
  def __init__(self):
    super().__init__("Sigma")

  def calculate(self, data,rounds = 14):
    df = pd.DataFrame(index = data.index)
    df['Close'] = data['Close']
    df[self.name] = df.Close.pct_change().rolling(rounds).std()
    self.output = df[self.name]
    return self.output

  def calc_buy_signals(self):
    return np.where(self.output > 0.01, True, False)
  
  def calc_sell_signals(self):
    return np.where(self.output < 55, True, False)
