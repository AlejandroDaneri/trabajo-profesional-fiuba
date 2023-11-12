import numpy as np
import pandas as pd

def RSI(data, rounds = 14):
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

def MACD(data, slow = 23, fast = 12, suavizado = 9):
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

def SIGMA(data, n = 40):
    df = pd.DataFrame(index = data.index)
    df['Close'] = data['Close']
    df['sigma'] = df.Close.pct_change().rolling(n).std()
    return df['sigma']

def CRUCE(data, fast = 20, slow = 60):
    df = pd.DataFrame(index = data.index)
    df['Close'] = data['Close']
    df['cruce'] = df.Close.rolling(fast).mean() / df.Close.rolling(slow).mean() - 1
    return df['cruce']
