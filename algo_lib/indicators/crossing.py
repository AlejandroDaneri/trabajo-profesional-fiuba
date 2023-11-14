from algo_lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd

class MACD(Indicator):
  def __init__(self, q):
    super().__init__(q)

  def calc(data, fast = 20, slow = 60):
    df = pd.DataFrame(index = data.index)
    df['Close'] = data['Close']
    df['cruce'] = df.Close.rolling(fast).mean() / df.Close.rolling(slow).mean() - 1
    return df['cruce']