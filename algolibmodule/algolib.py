print("Trabajo Profesional | Algo Trading | Libreria")

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

class AlgoLib:
    def __init__(self, ticker, start_date):
        self.data = yf.download(ticker, auto_adjust=True, start = start_date)

    def get_data(self):
        return self.data

    def RSI(self, rounds):
        data = self.data
        ## calcula la diferencia del price close entre la fila actual y la anterior
        data['diff'] = data.Close.diff()
        ## si la diferencia es mayor a 0 setea de cuanto fue, sino es ganancia pone 0
        data['win'] = np.where(data['diff'] > 0, data['diff'], 0)
        ## si la diferencia es menor a 0 setea de cuanto fue pero en valor absoluto, sino es ganancia pone 0
        data['loss'] = np.where(data['diff'] < 0, abs(data['diff']), 0)
        ## se calcula una media movil exponencial de las ganancias
        data['EMA_win'] = data.win.ewm(alpha = 1/rounds).mean()
        ## se calcula una media movil exponencial de las perdidas
        data['EMA_loss'] = data.loss.ewm(alpha = 1/rounds).mean()
        ## cociente entre ellas
        data['RS'] = data.EMA_win / data.EMA_loss
        ## se calcula finalmente el RSI
        data['RSI'] = 100 - (100 / (1 + data.RS))
        return data

    def MACD(self, slow = 23, fast = 12, suavizado = 9):
        data = self.data
        ## se calcula una media movil exponencial rapida
        data["ema_fast"] = data.Close.ewm(span = fast).mean()
        ## se calcula una media movil exponencial lenta
        data["ema_slow"] = data.Close.ewm(span = slow).mean()
        ## la resta de las medias moviles es otra media movil llamada macd
        data["macd"] = data.ema_fast - data.ema_slow
        ## a esta ultima se la suaviza y se la pasa a llamar signal
        data['signal'] = data.macd.ewm(span = suavizado).mean()
        ## finalmente el punto de interes es la diferencia entre la media movil macd y la señal
        ## particularmente es de interes cuando cruza el cero. 
        data['histogram'] = data.macd - data.signal
        data = data.dropna().round(2)
        return data
    
    def OBV(self, n):
        data['Balance'] = np.where(data.Close > data.Close.shift(), data['Volume'], np.where(data.Close < data.Close.shift(), -data['Volume'], 0))
        data['OBV'] = data['Balance'].rolling(n).sum()
        data['OBV_acotado'] = (data.OBV - data.OBV.rolling(n).min())/(data.OBV.rolling(n).max() - data.OBV.rolling(n).min())
        return data

    def plot_RSI(self):
        data = self.data
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data.RSI)
        plt.show()
    
    def plot_MACD(self):
        data = self.data
        fig = plt.figure()
        fig.set_size_inches(30, 5)
        plt.plot(data.macd)
        plt.show()