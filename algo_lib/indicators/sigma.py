from algo_lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd

class Sigma(Indicator):
  def __init__(self, q):
    super().__init__(q)

  def calculate(self, data,rounds = 14):
    df = pd.DataFrame(index = data.index)
    df['Close'] = data['Close']
    df[self.output] = df.Close.pct_change().rolling(rounds).std()
    self.output = df[self.name]
    return self.output
  
