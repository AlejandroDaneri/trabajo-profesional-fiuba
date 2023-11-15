from algo_lib.indicators.indicator import Indicator
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