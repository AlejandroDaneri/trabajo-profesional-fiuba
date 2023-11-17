from indicators.indicator import Indicator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class OBV(Indicator):
  def __init__(self):
    super().__init__("OBV")

  def calculate(self, data,n):
    df = pd.DataFrame(index=data.index)
    self.dates= data.index

    df['Balance'] = np.where(data.Close>data.Close.shift(),
                               data['Volume'],
                               np.where(data.Close<data.Close.shift(),-data['Volume'],0 ))   
    df[self.name] = df['Balance'].rolling(n).sum()
    self.output = df[self.name]

    return self.output