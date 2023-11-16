from indicators.indicator import Indicator
import numpy as np
import pandas as pd

class Crossing(Indicator):
  def __init__(self):
    super().__init__("Cruce")

  def calculate(self,data, fast = 20, slow = 60):
    df = pd.DataFrame(index = data.index)
    df['Close'] = data['Close']
    df[self.name] = df.Close.rolling(fast).mean() / df.Close.rolling(slow).mean() - 1
    self.output = df[self.name]
    return self.output
  
  def calc_sell_signal(self):
    return np.where(self.output < -0.01, True, False)

  def calc_buy_signals(self):
    return np.where(self.output > 0, True, False)