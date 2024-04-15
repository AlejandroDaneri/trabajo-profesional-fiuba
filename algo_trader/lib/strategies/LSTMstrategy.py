
from lib.actions import Action
from lib.indicators.indicator import Indicator
from lib.strategies.strategy import Strategy


import talib as ta
import pandas as pd
import numpy as np
from typing import List
import tensorflow as tf
from tensorflow import keras


class LSTM(Strategy):
    def __init__(self, indicators: List[Indicator]=[]):
        print(tf.__version__)
        self.name = "LSTM"

        self.model = keras.models.load_model("lstm_model_dnn")  # TODO: change hardcoded src

        super().__init__(indicators)

    
    def prepare_data(self, historical_data: pd.DataFrame):
        self.data = historical_data[["Open", "High", "Low", "Close","Volume"]].copy()
        self.data["High"] = self.data["High"].apply(lambda x: float(x))
        self.data["Low"] = self.data["Low"].apply(lambda x: float(x))
        self.data["Close"] = self.data["Close"].apply(lambda x: float(x))
        self.data["Volume"] = self.data["Volume"].apply(lambda x: float(x))
        self.data["Open"] = self.data["Open"].apply(lambda x: float(x))

    def _reshape(self,data, time_steps):
        samples = len(data) - time_steps + 1
        reshaped_data = np.zeros((samples, time_steps, data.shape[1]))
        for i in range(samples):
            reshaped_data[i] = data[i:i + time_steps]
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
        new_record['r'] = np.log(new_record['Close'] / new_record["Close"].shift(1))


        time_periods = [6, 8, 10, 12, 14, 16, 18, 22, 26, 33, 44, 55]
        name_periods = [6, 8, 10, 12, 14, 16, 18, 22, 26, 33, 44, 55]

        df = new_record.copy()

        for period in time_periods:
            for nperiod in name_periods:
                df[f'ATR_{nperiod}'] = ta.ATR(df['High'], df['Low'], df['Close'], timeperiod=period)
                df[f'EMA_{nperiod}'] = ta.EMA(df['Close'], timeperiod=period)
                df[f'RSI_{nperiod}'] = ta.RSI(df['Close'], timeperiod=period)
                df[f'VWAP_{nperiod}'] = ta.SUM(df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3, timeperiod=period) / ta.SUM(df['Volume'], timeperiod=period)
                df[f'ROC_{nperiod}'] = ta.ROC(df['Close'], timeperiod=period)
                df[f'KC_upper_{nperiod}'] = ta.EMA(df['High'], timeperiod=period)
                df[f'KC_middle_{nperiod}'] = ta.EMA(df['Low'], timeperiod=period)
                df[f'Donchian_upper_{nperiod}'] = ta.MAX(df['High'], timeperiod=period)
                df[f'Donchian_lower_{nperiod}'] = ta.MIN(df['Low'], timeperiod=period)
                macd, macd_signal, _ = ta.MACD(df['Close'], fastperiod=(period + 12), slowperiod=(period + 26), signalperiod=(period + 9))
                df[f'MACD_{nperiod}'] = macd
                df[f'MACD_signal_{nperiod}'] = macd_signal
                bb_upper, bb_middle, bb_lower = ta.BBANDS(df['Close'], timeperiod=period, nbdevup=2, nbdevdn=2)
                df[f'BB_upper_{nperiod}'] = bb_upper
                df[f'BB_middle_{nperiod}'] = bb_middle
                df[f'BB_lower_{nperiod}'] = bb_lower
                df[f'EWO_{nperiod}'] = ta.SMA(df['Close'], timeperiod=(period+5)) - ta.SMA(df['Close'], timeperiod=(period+35))

        self.data = pd.concat([self.data, new_record])

        new_record = self._reshape(df, 1)

        prediction = self.model.predict(new_record)

        m_signal = np.argmax(np.argmax(prediction, axis=1))
        signal = 1 if m_signal == 1 else -1
        if signal == -1:
            signal = Action.SELL
        elif signal == 1:
            signal = Action.BUY
        else:
            signal = Action.HOLD
        print(f'[Strategy | LSTM] Signal: {signal}')
        return signal
