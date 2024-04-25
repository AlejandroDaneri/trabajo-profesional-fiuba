
from lib.actions import Action
from lib.indicators.indicator import Indicator
from lib.strategies.strategy import Strategy
# from sklearn.preprocessing import MinMaxScaler

from lib.indicators.atr import ATR
from lib.indicators.ema import EMA
from lib.indicators.rsi import RSI
from lib.indicators.vwap import VWAP
from lib.indicators.roc import ROC
from lib.indicators.kc import KC
from lib.indicators.donchian import DONCHIAN
from lib.indicators.macd import MACD
from lib.indicators.bbands import BBANDS
from lib.indicators.ewo import EWO

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

            atr = ATR(period)
            atr_df = atr.calculate(self.data)

            ema = EMA(period)
            ema_df = ema.calculate(self.data)

            rsi = RSI(30, 70, period)
            rsi_df = rsi.calculate(self.data)

            vwap = VWAP(period)
            vwap_df = vwap.calculate(self.data)

            roc = ROC(period)
            roc_df = roc.calculate(self.data)

            kc = KC(period, period, 2, 0.08)
            kc_df = kc.calculate(self.data)

            donchian = DONCHIAN(period, 0.05)
            donchian_df = donchian.calculate(self.data)

            macd = MACD(period + 26, period + 12, period + 9)
            macd_df = macd.calculate(self.data)

            bbands = BBANDS(period, 2)
            bbands_df = bbands.calculate(self.data)

            ewo = EWO(period+5, period+35)
            ewo_df = ewo.calculate(self.data)

            for nperiod in name_periods:
                data[f'ATR_{nperiod}'] = atr_df
                data[f'EMA_{nperiod}'] = ema_df["EMA"]
                data[f'RSI_{nperiod}'] = rsi_df
                data[f'VWAP_{nperiod}'] = vwap_df["VWAP"]
                data[f'ROC_{nperiod}'] = roc_df["ROC"]
                data[f'KC_upper_{nperiod}'] = kc_df["UpperBand"]
                data[f'KC_lower_{nperiod}'] = kc_df["LowerBand"]
                data[f'Donchian_upper_{nperiod}'] = donchian_df["HighChannel"]
                data[f'Donchian_lower_{nperiod}'] = donchian_df["LowChannel"]
                data[f'MACD_{nperiod}'] = macd_df["histogram"]
                data[f'MACD_signal_{nperiod}'] = macd_df["signal"]
                data[f'BB_upper_{nperiod}'] = bbands_df["UpperBand"]
                data[f'BB_middle_{nperiod}'] = bbands_df["MidBand"]
                data[f'BB_lower_{nperiod}'] = bbands_df["LowerBand"]
                data[f'EWO_{nperiod}'] = ewo_df["EWO"]

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
