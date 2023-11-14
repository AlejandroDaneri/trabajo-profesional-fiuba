from algo_lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd

class RSI(Indicator):
  def __init__(self, q):
    super().__init__(q)

  def calc(self, data,rounds = 14):
    df = pd.DataFrame(index = data.index)
    df['Close'] = data['Close']
    # calcula la diferencia del price close entre la fila actual y la anterior
    df['diff'] = df.Close.diff()
    # si la diferencia es mayor a 0 setea de cuanto fue, sino es ganancia pone 0
    df['win'] = np.where(df['diff'] > 0, df['diff'], 0)
    # si la diferencia es menor a 0 setea de cuanto fue pero en valor absoluto, sino es ganancia pone 0
    df['loss'] = np.where(df['diff'] < 0, abs(df['diff']), 0)
    # se calcula una media movil exponencial de las ganancias
    df['EMA_win'] = df.win.ewm(alpha = 1/rounds).mean()
    # se calcula una media movil exponencial de las perdidas
    df['EMA_loss'] = df.loss.ewm(alpha = 1/rounds).mean()
    # cociente entre ellas
    df['RS'] = df.EMA_win / df.EMA_loss
    # se calcula finalmente el RSI
    df['RSI'] = 100 - (100 / (1 + df.RS))
    return df['RSI']
