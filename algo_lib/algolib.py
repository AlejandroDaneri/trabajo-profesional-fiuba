print("Trabajo Profesional | Algo Trading | Libreria")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def get_data(ticker, start_date):
    return yf.download(ticker, auto_adjust=True, start = start_date)

def get_gatillos_compra(data, features):
    gatillos_compra = pd.DataFrame(index = data.index)
    for feature in features:
        if feature == 'rsi':
            gatillos_compra['rsi'] = np.where(data['rsi'] > 65, True, False)
        elif feature == 'sigma':
            gatillos_compra['sigma'] = np.where(data['sigma'] > 0.01, True, False)
        elif feature == 'cruce':
            gatillos_compra['cruce'] = np.where(data['cruce'] > 0, True, False)
    gatillos_compra['all'] = gatillos_compra.all(axis=1)
    return gatillos_compra

def get_gatillos_venta(data, features):
    gatillos_venta = pd.DataFrame(index = data.index)
    for feature in features:
        if feature == 'rsi':
            gatillos_venta['rsi'] = np.where(data['rsi'] < 55, True, False)
        elif feature == 'cruce':
            gatillos_venta['cruce'] = np.where(data['cruce'] < -0.01, True, False)
    gatillos_venta['all'] = gatillos_venta.all(axis=1)
    return gatillos_venta

def get_acciones(gatillos_compra, gatillos_venta):
    gatillos = pd.DataFrame(index = gatillos_compra.index)
    mascara_compra = gatillos_compra['all']
    mascara_venta = gatillos_venta['all']
    # definimos para cada dia si se dispara un gatillo de compra o de venta, o ninguno de los dos
    gatillos['gatillo'] = np.where(mascara_compra, 'compra', np.where(mascara_venta, 'venta', ''))
    # un nuevo dataframe con las filas filtradas para las cuales no habia ni gatillo de compra ni de venta
    acciones = gatillos.loc[gatillos['gatillo'] != ''].copy()
    # detecto si el gatillo se repite entre la fila actual y la anterior, si es asi lo dejo como esta, sino lo pongo en blanco
    acciones['gatillo'] = np.where(acciones.gatillo != acciones.gatillo.shift(), acciones.gatillo, '')
    # gracias a la paso anterior puedo detectar gatillos repetidos, procedo a filtrarlos
    acciones = acciones.loc[acciones.gatillo != ''].copy()
    return acciones

    def backtesting(self, indicator = 'RSI', trig_buy=65, trig_sell=55):
        # por ahora estrategia unicamente utilizando rsi
        data = self.data
        data.dropna(inplace=True) 

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