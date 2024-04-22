
from lib.actions import Action
from lib.indicators.indicator import Indicator
from lib.strategies.strategy import Strategy
# from sklearn.preprocessing import MinMaxScaler


import talib as ta
import pandas as pd
import numpy as np
from typing import List
import tensorflow as tf
from tensorflow import keras
import time
class LSTM(Strategy):
    def __init__(self, indicators: List[Indicator], timeframe: str, id: str):
        self.name = "LSTM"

        self.model = keras.models.load_model("lstm_model_dnn")  # TODO: change hardcoded src
        print(self.model)
        super().__init__([], timeframe, id)

    
    def prepare_data(self, historical_data: pd.DataFrame):
        print("LSTM| begin prepare")
        self.data = historical_data[["Open", "High", "Low", "Close","Volume"]].copy()
        self.data["High"] = self.data["High"].apply(lambda x: float(x))
        self.data["Low"] = self.data["Low"].apply(lambda x: float(x))
        self.data["Close"] = self.data["Close"].apply(lambda x: float(x))
        self.data["Volume"] = self.data["Volume"].apply(lambda x: float(x))
        self.data["Open"] = self.data["Open"].apply(lambda x: float(x))
        print("LSTM| end prepare")

    def _reshape(self, data, time_steps):
        saved_params = pd.read_csv('scaling_params.csv')

        min_vals = saved_params['min_values'].values
        max_vals = saved_params['max_values'].values
        new_data_scaled = (data - min_vals) / (max_vals - min_vals)
        samples = len(new_data_scaled) - time_steps + 1
        reshaped_data = np.zeros((samples, time_steps, new_data_scaled.shape[1]))
        for i in range(samples):
            reshaped_data[i] = new_data_scaled[i:i + time_steps]
        return reshaped_data

    def _get_state(self):
        return self.data_std[self.features].iloc[-self.lags :]

    def predict(self, new_record: pd.DataFrame):
        new_record = new_record[["Open", "High", "Low", "Close","Volume"]].copy()
        new_record["Close"] = new_record["Close"].apply(lambda x: float(x))
        new_record["High"] = new_record['High'].apply(lambda x: float(x))
        new_record["Low"] = new_record['Low'].apply(lambda x: float(x))
        new_record["Open"] = new_record['Open'].apply(lambda x: float(x))
        new_record["Volume"] = new_record['Volume'].apply(lambda x: float(x))
        print("LSTM| Prediction")
        self.data = pd.concat([self.data, new_record])

        time_periods = [6, 8, 10, 12, 14, 16, 18, 22, 26, 33, 44, 55]
        name_periods = [6, 8, 10, 12, 14, 16, 18, 22, 26, 33, 44, 55]

        data = {}
        data['r'] = np.log(self.data['Close'] / self.data["Close"].shift(1))
        for period in time_periods:
            print("LSTM| period: ",period)

            for nperiod in name_periods:
                data[f'ATR_{nperiod}'] = ta.ATR(self.data['High'], self.data['Low'], self.data['Close'], timeperiod=period)
                data[f'EMA_{nperiod}'] = ta.EMA(self.data['Close'], timeperiod=period)
                data[f'RSI_{nperiod}'] = ta.RSI(self.data['Close'], timeperiod=period)
                data[f'VWAP_{nperiod}'] = ta.SUM(self.data['Volume'] * (self.data['High'] + self.data['Low'] + self.data['Close']) / 3, timeperiod=period) / ta.SUM(self.data['Volume'], timeperiod=period)
                data[f'ROC_{nperiod}'] = ta.ROC(self.data['Close'], timeperiod=period)
                data[f'KC_upper_{nperiod}'] = ta.EMA(self.data['High'], timeperiod=period)
                data[f'KC_middle_{nperiod}'] = ta.EMA(self.data['Low'], timeperiod=period)
                data[f'Donchian_upper_{nperiod}'] = ta.MAX(self.data['High'], timeperiod=period)
                data[f'Donchian_lower_{nperiod}'] = ta.MIN(self.data['Low'], timeperiod=period)
                macd, macd_signal, _ = ta.MACD(self.data['Close'], fastperiod=(period + 12), slowperiod=(period + 26), signalperiod=(period + 9))
                data[f'MACD_{nperiod}'] = macd
                data[f'MACD_signal_{nperiod}'] = macd_signal
                bb_upper, bb_middle, bb_lower = ta.BBANDS(self.data['Close'], timeperiod=period, nbdevup=2, nbdevdn=2)
                data[f'BB_upper_{nperiod}'] = bb_upper
                data[f'BB_middle_{nperiod}'] = bb_middle
                data[f'BB_lower_{nperiod}'] = bb_lower
                data[f'EWO_{nperiod}'] = ta.SMA(self.data['Close'], timeperiod=(period+5)) - ta.SMA(self.data['Close'], timeperiod=(period+35))

        new_df = pd.DataFrame.from_dict(data, orient='columns')

        output = pd.concat([self.data, new_df],axis=1)

        new_record = self._reshape(output.tail(1), 1)

        prediction = self.model.predict(new_record)

        m_signal = np.argmax(prediction[0])
        print(prediction[0])

        signal = 1 if m_signal == 1 else -1
        if signal == -1:
            signal = Action.SELL
        elif signal == 1:
            signal = Action.BUY
        else:
            signal = Action.HOLD
        print("signal", signal)
        return signal
