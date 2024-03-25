from lib.indicators.indicator import Indicator
from lib.utils.plotter import plot_df
from lib.indicators.ema import EMA

import pandas as pd

class MeanReversionOscilatorEma100(Indicator):
    def __init__(self, buy_threshold, sell_threshold, window):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.window = window
        super().__init__("MeanReversionOscilatorEma100")

    def calculate(self, data, normalize=False):
        # Create a DataFrame with the same index as the input data
        self.data = data
        df = pd.DataFrame(index=data.index)
        self.dates = data.index
        df["Close"] = data["Close"]

        # calculates EMA 100
        indicator_ema = EMA(100)
        df["ema_100"] = indicator_ema.calculate(data)["EMA"]

        # calculates the OSCILATOR using Z-Score method
        df["diff"] = df["Close"] - df["ema_100"]
        media = df["diff"].rolling(self.window).mean()
        desviacion_estandar = df["diff"].rolling(self.window).std()
        df['z_score'] = (df["diff"] - media) / desviacion_estandar

        self.df_output = df
        return self.df_output

    def calc_buy_signals(self):
        df = self.df_output
        buy_condition = (df['z_score'].shift(1) < self.buy_threshold) & (df['z_score'] >= self.buy_threshold)
        return self._calc_buy_signals(buy_condition)

    def calc_sell_signals(self):
        df = self.df_output
        sell_condition = (df['z_score'].shift(1) < self.sell_threshold) & (df['z_score'] >= self.sell_threshold)
        return self._calc_sell_signals(sell_condition)

    def plot(self, log_scale=False):
        df = self.df_output
        plot_df(self.data.index, df, log_scale=log_scale)

    def predict_signal(self, new_record, as_enum=True):
        new_df = self.calculate(pd.concat([self.data, new_record]))

        new_signal = new_df.iloc[-1]

        print(f"[Crossing SMA] Current fast SMA value: {new_signal.FAST_SMA}")
        print(f"[Crossing SMA] Current slow SMA value: {new_signal.SLOW_SMA}")

        signal = self.get_last_signal(as_enum)

        print(f"[Crossing SMA] Signal: {signal}")

        return signal
