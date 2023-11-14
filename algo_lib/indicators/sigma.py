from algo_lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd

class RSI(Indicator):
  def __init__(self, q):
    super().__init__(q)

  def calc(self, data,rounds = 14):
    df = pd.DataFrame(index = data.index)
    df['Close'] = data['Close']
    df['sigma'] = df.Close.pct_change().rolling(rounds).std()
    return df['sigma']
