import numpy as np
import pandas as pd
import yfinance as yf

def getActions(data, features, trig_buy_cross=0, trig_buy_rsi=65, trig_buy_sigma=0.01,
               trig_sell_cross=-0.01, trig_sell_rsi=55, trig_sell_obv=0):
    
    buy_triggers = pd.DataFrame(index=features.index)
    buy_triggers['cross'] = features['cross'] > trig_buy_cross
    buy_triggers['rsi'] = features['rsi'] > trig_buy_rsi
    buy_triggers['sigma'] = features['sigma'] > trig_buy_sigma
    buy_mask = buy_triggers.all(axis=1)

    sell_triggers = pd.DataFrame(index=features.index)
    sell_triggers['cross'] = features['cross'] < trig_sell_cross
    sell_triggers['rsi'] = features['rsi'] < trig_sell_rsi
    sell_triggers['obv'] = features['OBV_osc'] > trig_sell_obv
    sell_mask = sell_triggers.all(axis=1)

    data.dropna(inplace=True)

    data['signal'] = np.where(buy_mask, 'buy', np.where(sell_mask, 'sell', ''))
    actions = data.loc[data['signal'] != ''].copy()

    actions['signal'] = np.where(actions['signal'] != actions['signal'].shift(), actions['signal'], "")
    actions = actions.loc[actions['signal'] != ''].copy()

    if actions.iloc[0]['signal'] == 'sell':
        actions = actions.iloc[1:]
    if actions.iloc[-1]['signal'] == 'buy':
        actions = actions.iloc[:-1]
    
    return actions

def getTrades(actions):
    evens = actions.iloc[::2][['Close']].reset_index()
    odds = actions.iloc[1::2][['Close']].reset_index()
    trades = pd.concat([evens, odds], axis=1)

    transaction_cost =0
    trades.columns = ['buy_date', 'buy_price', 'sell_date', 'sell_price'] 
    trades['return'] = trades['sell_price'] / trades['buy_price'] - 1

    trades['return'] -= transaction_cost
    trades['days'] = (trades['sell_date'] - trades['buy_date']).dt.days

    if len(trades) > 0:
        trades['result'] = np.where(trades['return'] > 0, 'Winner', 'Loser')
        trades['cumulative_return'] = (trades['return'] + 1).cumprod() - 1

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

    data['cross'] = data['Close'].rolling(fast).mean() / data['Close'].rolling(slow).mean() - 1
    data['rsi'] = 100 - (100 / (1 + rs))
    data['sigma'] = data['Close'].pct_change().rolling(n_sigma).std()
    data['OBV_osc'] = (data['OBV'] - data['OBV'].rolling(n_obv).mean()) / data['OBV'].rolling(n_obv).std()

    features = data.iloc[:, -4:].dropna()
    return features

def eventDriveLong(df): 
    df["pct_change"]=df['Close'].pct_change() 
    signals=df['signal'].tolist()
    pct_changes =df['pct_change'].tolist()

    total = len(signals) 
    i, results = 1, [0]

    while i<total:

        if signals[i-1] == 'buy':
            j=i
            while j<total:
                results.append(pct_changes[j])
                j +=1
                if signals[j-1]=="sell":
                    i=j
                    break
                if j == total:
                    i=j
                    print("Open buy")
                    break

        else:
            results.append(0)
            i +=1

    result = pd.concat([df,pd.Series(data=results,index=df.index)],axis=1)
    result.columns.values[-1] ="strategy"
    return result
