print("Trabajo Profesional | Algo Trading | Libreria")

import numpy as np

def get_prizes_from_binance():
    return '100k'

def RSI(data, rounds):
    data['diff']= data.Close.diff()
    data['win']= np.where(data['diff']>0,data['diff'],0)
    data['loss']= np.where(data['diff']<0,abs(data['diff']),0)
    data['EMA_win'] = data.win.ewm(alpha=1/rounds).mean()
    data['EMA_loss'] = data.loss.ewm(alpha=1/rounds).mean()
    data['RS'] = data.EMA_win / data.EMA_loss
    data['RSI'] = 100 - (100 /1+data.RS)
    data