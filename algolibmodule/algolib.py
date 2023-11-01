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
        data['diff'] = data.Close.diff()
        data['win'] = np.where(data['diff']>0, data['diff'],0)
        data['loss'] = np.where(data['diff']<0,abs(data['diff']),0)
        data['EMA_win'] = data.win.ewm(alpha=1/rounds).mean()
        data['EMA_loss'] = data.loss.ewm(alpha=1/rounds).mean()
        data['RS'] = data.EMA_win / data.EMA_loss
        data['RSI'] = 100 - (100 /(1 + data.RS))
        return data

    """
    ### Moving Average Converge Divergence ###

                FAST   - SLOW
    MACD LINE = EMA 12 - EMA 23
    
    SIGNAL = EMA 9 (MACD LINE)
    MACD = SIGNAL - MACD LINE

    ##########################################
    """
    def MACD(self, slow = 23, fast = 12, suavizado = 9):
        data = self.data
        data["ema_fast"] = data.Close.ewm(span=fast).mean()
        data["ema_slow"] = data.Close.ewm(span=slow).mean()
        data["macd"] = data.ema_fast - data.ema_slow
        data['signal'] = data.macd.ewm(span=suavizado).mean()
        data['histogram'] = data.macd - data.signal
        data = data.dropna().round(2)
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