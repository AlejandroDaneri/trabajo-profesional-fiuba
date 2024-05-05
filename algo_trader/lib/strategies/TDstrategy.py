from lib.actions import Action
from lib.indicators.indicator import Indicator
from lib.strategies.strategy import Strategy
from lib.strategies.base_strategies.TrendDetectionBase import TrendDetectionBase
from typing import List
from collections import Counter

import pandas as pd
import numpy as np

class TDstrategy(Strategy):
    def __init__(self, indicators: List[Indicator], timeframe: str, id: str):
        self.name = "TD"

        # TODO: check to parameterize this data
        self.rounds_ema = 14
        self.rounds_dmi = 5
        self.rounds_adx = 5
        self.threshold_adx = 20
        self.period_slope = 5
        self.tdb = TrendDetectionBase(self.rounds_ema, self.rounds_dmi, self.rounds_adx, self.threshold_adx, self.period_slope)   

        super().__init__(indicators, timeframe, id)

    def prepare_data(self, historical_data: pd.DataFrame):
        print(self.name + " | begin prepare")
        self.data = historical_data[["Open", "High", "Low", "Close","Volume"]].copy()
        self.data["High"] = self.data["High"].apply(lambda x: float(x))
        self.data["Low"] = self.data["Low"].apply(lambda x: float(x))
        self.data["Close"] = self.data["Close"].apply(lambda x: float(x))
        self.data["Volume"] = self.data["Volume"].apply(lambda x: float(x))
        self.data["Open"] = self.data["Open"].apply(lambda x: float(x))        
        print(self.name + " | end prepare")

    def predict(self, new_record):
        new_record = new_record[["Open", "High", "Low", "Close","Volume"]].copy()
        new_record["High"] = new_record["High"].apply(lambda x: float(x))
        new_record["Low"] = new_record["Low"].apply(lambda x: float(x))
        new_record["Close"] = new_record["Close"].apply(lambda x: float(x))
        new_record["Volume"] = new_record["Volume"].apply(lambda x: float(x))
        new_record["Open"] = new_record["Open"].apply(lambda x: float(x))

        print(self.name + " | prediction")

        self.data = pd.concat([self.data, new_record])

        confirmed_signals_df = self.tdb.get_confirmed_signals(self.data)

        signals = []
        
        for indicator in self.indicators:
            indicator.calculate(self.data, False)
            indicator_signals = indicator.generate_signals()
            PointEntry = np.where((indicator_signals == 1) & (confirmed_signals_df["ConfirmedEntrySignal"] != np.nan), 1, 0)
            PointExit = np.where((indicator_signals == -1) & (confirmed_signals_df["ConfirmedOutputSignal"] != np.nan), -1, 0)
            signal = PointEntry + PointExit
            signals.append(signal[signal.size -1])

        signal_counter = Counter(signals)
        result_signal = signal_counter.most_common(1)[0][0]

        if result_signal == -1:
            result_signal = Action.SELL
        elif result_signal == 1:
            result_signal = Action.BUY
        else:
            result_signal = Action.HOLD
        print("signal", result_signal)
        return result_signal
    