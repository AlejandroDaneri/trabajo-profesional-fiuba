
from flask import Flask
import numpy as np
import pandas as pd

app = Flask(__name__)
def getTrades(actions):
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
        trades['resultado']= np.where(trades['rendimiento' ] > 0, 'Ganador', 'Perdedor')
        trades['rendimientoAcumulado'] = (trades['rendimiento']+1).cumprod()-1

    return trades
@app.route('/')
def hello_world():
    return 'Hello, World!'
