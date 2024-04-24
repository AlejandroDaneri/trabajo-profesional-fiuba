from flask import Flask, jsonify
import numpy as np
import pandas as pd
import yfinance as yf

app = Flask(__name__)

def getActions(data, features, trig_buy_cross=0, trig_buy_rsi=65, trig_buy_sigma=0.01,
               trig_sell_cross=-0.01, trig_sell_rsi=55, trig_sell_obv=0):
    
    gatillos_compra = pd.DataFrame(index=features.index)
    gatillos_compra['cruce'] = features['cruce'] > trig_buy_cross
    gatillos_compra['rsi'] = features['rsi'] > trig_buy_rsi
    gatillos_compra['sigma'] = features['sigma'] > trig_buy_sigma
    mascara_compra = gatillos_compra.all(axis=1)

    gatillos_venta = pd.DataFrame(index=features.index)
    gatillos_venta['cruce'] = features['cruce'] < trig_sell_cross
    gatillos_venta['rsi'] = features['rsi'] < trig_sell_rsi
    gatillos_venta['obv'] = features['OBV_osc'] > trig_sell_obv
    mascara_venta = gatillos_venta.all(axis=1)

    data_aux = data.copy().dropna()

    data_aux['gatillo'] = np.where(mascara_compra, 'compra', np.where(mascara_venta, 'venta', ''))
    actions = data_aux.loc[data_aux['gatillo'] != ''].copy()

    actions['gatillo'] = np.where(actions['gatillo'] != actions['gatillo'].shift(), actions['gatillo'], "")
    actions = actions.loc[actions['gatillo'] != ''].copy()

    if actions.iloc[0]['gatillo'] == 'venta':
        actions = actions.iloc[1:]
    if actions.iloc[-1]['gatillo'] == 'compra':
        actions = actions.iloc[:-1]
    
    return actions

def getTrades(actions):
    pares = actions.iloc[::2][['Close']].reset_index()
    impares = actions.iloc[1::2][['Close']].reset_index()
    trades = pd.concat([pares, impares], axis=1)

    CT = 0
    trades.columns = ['fecha_compra', 'px_compra', 'fecha_venta', 'px_venta'] 
    trades['rendimiento'] = trades['px_venta'] / trades['px_compra'] - 1
    trades['rendimiento'] -= CT
    trades['dias'] = (trades['fecha_venta'] - trades['fecha_compra']).dt.days

    if len(trades) > 0:
        trades['resultado'] = np.where(trades['rendimiento'] > 0, 'Ganador', 'Perdedor')
        trades['rendimientoAcumulado'] = (trades['rendimiento'] + 1).cumprod() - 1

    return trades

def getData(ticker, data_from, data_to):
    data = yf.download(ticker, auto_adjust=True, progress=False, start=data_from, end=data_to)
    return data

def getFeatures(data, n_obv=100, n_sigma=40, n_rsi=15, fast=20, slow=60):
    data['Balance'] = np.where(data['Close'] > data['Close'].shift(), data['Volume'],
                                np.where(data['Close'] < data['Close'].shift(), -data['Volume'], 0))

    data['OBV'] = data['Balance'].cumsum()
    dif = data['Close'].diff()
    win = pd.DataFrame(np.where(dif > 0, dif, 0), index=data.index) 
    loss = pd.DataFrame(np.where(dif < 0, abs(dif), 0), index=data.index)
    ema_win = win.ewm(alpha=1/n_rsi).mean()
    ema_loss = loss.ewm(alpha=1/n_rsi).mean()
    rs = ema_win / ema_loss

    data['cruce'] = data['Close'].rolling(fast).mean() / data['Close'].rolling(slow).mean() - 1
    data['rsi'] = 100 - (100 / (1 + rs))
    data['sigma'] = data['Close'].pct_change().rolling(n_sigma).std()
    data['OBV_osc'] = (data['OBV'] - data['OBV'].rolling(n_obv).mean()) / data['OBV'].rolling(n_obv).std()

    features = data.iloc[:, -4:].dropna()
    return features

@app.route('/')
def hello_world():
    data = getData(ticker='SOL-USD', data_from='2021-01-01', data_to='2023-05-05')
    features = getFeatures(data, n_obv=100, n_sigma=40, n_rsi=15, fast=20, slow=60)
    actions = getActions(data, features, 0, 65, 0.01, -0.01, 55, 0)
    trades = getTrades(actions)
    trades_dict = trades.to_dict(orient='records')
    
    return jsonify(trades_dict)
    
