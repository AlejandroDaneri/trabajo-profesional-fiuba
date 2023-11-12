print("Trabajo Profesional | Algo Trading | Libreria")

import pandas as pd
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
        # calcula la diferencia del price close entre la fila actual y la anterior
        data['diff'] = data.Close.diff()
        # si la diferencia es mayor a 0 setea de cuanto fue, sino es ganancia pone 0
        data['win'] = np.where(data['diff'] > 0, data['diff'], 0)
        # si la diferencia es menor a 0 setea de cuanto fue pero en valor absoluto, sino es ganancia pone 0
        data['loss'] = np.where(data['diff'] < 0, abs(data['diff']), 0)
        # se calcula una media movil exponencial de las ganancias
        data['EMA_win'] = data.win.ewm(alpha = 1/rounds).mean()
        # se calcula una media movil exponencial de las perdidas
        data['EMA_loss'] = data.loss.ewm(alpha = 1/rounds).mean()
        # cociente entre ellas
        data['RS'] = data.EMA_win / data.EMA_loss
        # se calcula finalmente el RSI
        data['RSI'] = 100 - (100 / (1 + data.RS))
        return data

    def MACD(self, slow = 23, fast = 12, suavizado = 9):
        data = self.data
        # se calcula una media movil exponencial rapida
        data["ema_fast"] = data.Close.ewm(span = fast).mean()
        # se calcula una media movil exponencial lenta
        data["ema_slow"] = data.Close.ewm(span = slow).mean()
        # la resta de las medias moviles es otra media movil llamada macd
        data["macd"] = data.ema_fast - data.ema_slow
        # a esta ultima se la suaviza y se la pasa a llamar signal
        data['signal'] = data.macd.ewm(span = suavizado).mean()
        # finalmente el punto de interes es la diferencia entre la media movil macd y la señal
        # particularmente es de interes cuando cruza el cero. 
        data['histogram'] = data.macd - data.signal
        data = data.dropna().round(2)
        return data

    def backtesting(self, indicator = 'RSI', trig_buy=65, trig_sell=55):
        # por ahora estrategia unicamente utilizando rsi
        data = self.data
        data.dropna(inplace=True) 

        # calculo el RSI
        self.RSI(14)
        gatillos_compra = pd.DataFrame(index = data.index)
        gatillos_venta = pd.DataFrame(index = data.index)

        # creo columna indicando si se el indicador da compra/venta en cada una de las filas
        gatillos_compra[indicator] = np.where(data[indicator] > trig_buy, True, False)
        gatillos_venta[indicator] = np.where(data[indicator]  < trig_sell, True, False)

        mascara_compra = gatillos_compra.all(axis=1)
        mascara_venta = gatillos_venta.all(axis=1)

        data['gatillo'] = np.where(mascara_compra, 'compra', np.where(mascara_venta, 'venta', ''))
        actions = data.loc[data.gatillo != ''].copy()
        actions['gatillo'] = np.where(actions.gatillo != actions.gatillo.shift(), actions.gatillo, "")
        actions = actions.loc[actions.gatillo !=''].copy() 

        if actions.iloc[0].loc['gatillo'] == 'venta':
            actions = actions.iloc[1:]
        if actions.iloc[-1].loc['gatillo'] == 'compra':
            actions = actions.iloc[:-1]
            pares = actions.iloc[::2].loc[:,['Close']].reset_index()
        impares = actions.iloc[1::2].loc[:,['Close']].reset_index()
        trades = pd.concat([pares,impares],axis=1)
        trades
        CT=0

        trades.columns = ['fecha_compra', 'px_compra', 'fecha_venta','px_venta'] 

        trades['rendimiento'] = trades.px_venta / trades.px_compra - 1

        trades['rendimiento'] -=CT

        trades['dias'] = (trades.fecha_venta - trades.fecha_compra).dt.days
        if len(trades):
            trades['resultado'] = np.where(trades['rendimiento' ] > 0, 'Ganador', 'Perdedor')
            trades['rendimientoAcumulado'] = (trades['rendimiento']+1).cumprod()-1

        if len(trades):
            resultado = float(trades.iloc[-1].rendimientoAcumulado-1) 
            #agg_cant = trades.groupby('Nose').size()
            agg_rend = trades.groupby('resultado').mean()['rendimiento']
            agg_tiempos = trades.groupby('resultado').sum()['dias'] 
            agg_tiempos_medio = trades.groupby("resultado").mean()['dias']

            r = pd.concat([agg_rend, agg_tiempos, agg_tiempos_medio], axis=1) 
            r.columns = ['Rendimiento x Trade', 'Dias Total', 'Dias x Trade']
            resumen = r.T

            try:
                t_win = r['Dias Total']['Ganador']
            except:
                t_win = 0

            try:
                t_loss = r['Dias Total']['Perdedor']
            except:
                t_loss = 0

            t = t_win + t_loss

            tea = (resultado +1)*(365/t)-1 if t> 0 else 0

            metricas  = {'rendimiento':round(resultado,4), 'dias in':round(t,4), 'TEA':round(tea,4)}


        else:
            resumen = pd.DataFrame()
            metricas = {'rendimiento' :0, 'dias_in':0, 'TEA':0}
        print(actions)
        print(resumen) 
        print(metricas)

    
    def OBV(self, n):
        data['Balance'] = np.where(data.Close > data.Close.shift(), data['Volume'], np.where(data.Close < data.Close.shift(), -data['Volume'], 0))
        data['OBV'] = data['Balance'].rolling(n).sum()
        data['OBV_acotado'] = self.narror_indicator_by('min_dist',data['OBV'],n)
        return data
    
    def narror_indicator_by(self,type_,col,n):
        narrow_types = {
            'min_dist': (col - col.rolling(n).min())/(col.rolling(n).max() - col.rolling(n).min()),
            'z_scores_n_window': (col - col.rolling(n).mean())/(col.rolling(n).std()),
            'z_scores_all': (col - col.mean() / col.std())
        }
        return narrow_types.get(type_)
    


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