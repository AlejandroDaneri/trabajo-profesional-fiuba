from lib.indicators.ema import EMA
from lib.indicators.dmi import DMI
import numpy as np
import pandas as pd

class TrendDetectionBase():
    def __init__(self, rounds_ema, rounds_dmi, rounds_adx, threshold_adx, period_slope):
        self.rounds_ema = rounds_ema
        self.rounds_dmi = rounds_dmi
        self.rounds_adx = rounds_adx
        self.threshold_adx = threshold_adx
        self.period_slope = period_slope

    def get_confirmed_signals(self, data):
        df = pd.DataFrame(index=data.index)

        df['Open'] = data['Open']
        df['Close'] = data['Close']
        df['High'] = data['High']
        df['Low'] = data['Low']
        df['Volume'] = data['Volume']

        # Trend Detection
        ema = EMA(self.rounds_ema)
        ema_df = ema.calculate(df)
        df['EMA'] = ema_df.EMA
        df['Slope'] = self.calculate_slope(df['EMA'])

        # Trend Confirmation
        dmi = DMI(self.rounds_dmi, self.rounds_adx, self.threshold_adx)
        dmi_df = dmi.calculate(df)

        df['ADX'] = dmi_df['ADX']
        df['+di'] = dmi_df['+di']
        df['-di'] = dmi_df['-di']

        # Define the trend signals based on ADX
        df['TrendSignal+'] = np.where((self.threshold_adx < df.ADX) & (df['-di'] < df['+di']), 1, 0)
        df['TrendSignal-'] = np.where((self.threshold_adx < df.ADX) & (df['-di'] > df['+di']), -1, 0)
        df['TrendSignal'] = df['TrendSignal+'] + df['TrendSignal-']

        df['ConfirmedEntrySignal'] = np.where((0 < df.Slope) & (df["TrendSignal"] == 1), True, np.nan)
        df['ConfirmedOutputSignal'] = np.where((0 > df.Slope) & (df["TrendSignal"] == -1), True, np.nan)

        return df[['ConfirmedEntrySignal', 'ConfirmedOutputSignal']]

    def calculate_slope(self, series):
        slopes = []
        for i in range(0, len(series)):
            if (i < self.period_slope-1):
                slopes.append(0)
                continue
            x = np.arange(self.period_slope)
            y = series[i-self.period_slope+1:i+1].values

            # Calculate the slope using linear regression
            slope = np.polyfit(x, y, 1)[0]

            # Convert the slope to a percentage
            percent_slope = (slope / y[0]) * 100
            slopes.append(percent_slope)
        return slopes
    