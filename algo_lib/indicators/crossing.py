from indicators.indicator import Indicator
import numpy as np
import pandas as pd

class Crossing(Indicator):
  def __init__(self):
    super().__init__("Cruce")

  def calculate(self,data, fast = 20, slow = 60):
    df = pd.DataFrame(index = data.index)
    self.data=data
    df['Close'] = data['Close']
    df[self.name] = df.Close.rolling(fast).mean() / df.Close.rolling(slow).mean() - 1
    self.output = df[self.name]
    return self.output
  
  def calc_sell_signals(self):
    return np.where(self.output < -0.01, True, False)

  def calc_buy_signals(self):
    return np.where(self.output > 0, True, False)

  def predict_signal(self, new_record):
    # Calcular RSI para el DataFrame actualizado
    new_output = self.calculate(pd.concat([self.data, new_record]))

    # Extraer el valor de RSI para el nuevo registro
    new_signal = new_output.iloc[-1]
    # Tomar decisiones de trading basadas en el valor de RSI
    if new_signal  < -0.01:
        return "Sell"
    elif new_signal > 0:
        return "Buy"
    else:
        return "Hold"