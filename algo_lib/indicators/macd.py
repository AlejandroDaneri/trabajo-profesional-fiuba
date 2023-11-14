from algo_lib.indicators.indicator import Indicator
import numpy as np
import pandas as pd

class MACD(Indicator):
  def __init__(self, q):
    super().__init__(q)

  def calc(self, data,slow = 23, fast = 12, suavizado = 9):
    df = pd.DataFrame(index = data.index)
    df['Close'] = data['Close']
    # se calcula una media movil exponencial rapida
    df["ema_fast"] = df.Close.ewm(span = fast).mean()
    # se calcula una media movil exponencial lenta
    df["ema_slow"] = df.Close.ewm(span = slow).mean()
    # la resta de las medias moviles es otra media movil llamada macd
    df["macd"] = df.ema_fast - df.ema_slow
    # a esta ultima se la suaviza y se la pasa a llamar signal
    df['signal'] = df.macd.ewm(span = suavizado).mean()
    # finalmente el punto de interes es la diferencia entre la media movil macd y la señal
    # particularmente es de interes cuando cruza el cero. 
    df['histogram'] = df.macd - df.signal
    df = df.dropna().round(2)
    return df['histogram']