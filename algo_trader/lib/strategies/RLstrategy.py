from lib.actions import Action
from lib.indicators.indicator import Indicator
from lib.strategies.strategy import Strategy

import pandas as pd
import numpy as np
from typing import List
import tensorflow as tf
from tensorflow import keras


class RL(Strategy):
    def __init__(self, indicators: List[Indicator]):
        print(tf.__version__)
        self.name = "RL"

        self.model = keras.models.load_model("model")  # TODO: change hardcoded src
        self.lags = 15  # FIXME: add this info to model_info.csv

        df = pd.read_csv("model_info.csv")  # TODO: change hardcoded src

        self.mu = df["mu"]
        self.std = df["std"]

        self.features = [indicator.name for indicator in indicators]

        self.features.extend(["r"])
        self.n_features = len(self.features)
        super().__init__(indicators)

    def standarize(self, data):
        return (data - self.mu) / self.std

    def prepare_data(self, historical_data: pd.DataFrame):
        if len(historical_data) < self.lags:
            raise ValueError("Length of historical_data is less than self.lags")
        
        self.data = historical_data
        self.data["High"] = self.data["High"].apply(lambda x: float(x))
        self.data["Low"] = self.data["Low"].apply(lambda x: float(x))
        self.data["Close"] = self.data["Close"].apply(lambda x: float(x))
        self.data["Volume"] = self.data["Volume"].apply(lambda x: float(x))
        self.data["Open"] = self.data["Open"].apply(lambda x: float(x))

        self.data["r"] = np.log(self.data["Close"] / self.data["Close"].shift(1))
        for indicator in self.indicators:
            self.data[indicator.name] = None
            indicator.calculate(self.data, False)  
            self.data[indicator.name] = indicator.generate_signals()
        self.data = self.standarize(historical_data)

    def _reshape(self, state):
        return np.reshape(state, [1, self.lags, self.n_features])

    def _get_state(self):
        return self.data[self.features].iloc[-self.lags :]

    def predict(self, new_record: pd.Series):
        for indicator in self.indicators:
            new_record[indicator.name] = None
            new_record[indicator.name] = indicator.predict_signal(new_record, False)

        new_data = self.standarize(new_record)
        self.data = pd.concat([self.data, new_data])
        new_data = self._get_state()
        state = self._reshape(new_data.values)
        signal = np.argmax(self.model.predict(state)[0])
        if signal == -1:
            signal = Action.SELL
        elif signal == 1:
            signal = Action.BUY
        else:
            signal = Action.HOLD
        print("signal", signal)
        return signal
