from abc import abstractmethod

import numpy as np
from lib.actions import Action


class Indicator:
    def __init__(self, name):
        self.name = name
        return

    def calculate(self, data, normalize=False):
        if normalize:
            return self.normalize_output()
        return self.output

    @abstractmethod
    def predict_signal(self, new_record, as_enum=True):
        pass

    @abstractmethod
    def calc_buy_signals(self):
        pass

    @abstractmethod
    def calc_sell_signals(self):
        pass

    def _calc_buy_signals(self, condition):
        return np.where(condition, 1, 0)

    def _calc_sell_signals(self, condition):
        return np.where(
            condition,
            -1,
            0,
        )

    def normalize_output(self):
        mean = self.output.mean()
        std = self.output.std()
        return (self.output - mean) / std

    def generate_signals(self):
        buy_signals = self.calc_buy_signals()
        sell_signals = self.calc_sell_signals()

        return buy_signals + sell_signals

    def get_last_signal(self, as_enum=False):
        signal = self.generate_signals()[-1]
        if as_enum:
            if signal == -1:
                signal = Action.SELL
            elif signal == 1:
                signal = Action.BUY
            else:
                signal = Action.HOLD
        return signal

    @classmethod
    def hydrate(cls, parameters):
        required_params = cls.__init__.__code__.co_varnames[1:]  # Exclude 'self' parameter
        if parameters is None:
            print(f"Indicator {cls.__name__} does not have parameters")
            return None

        missing_params = [param for param in required_params if param not in parameters]
        if missing_params:
            print(f"Indicator {cls.__name__} is missing required parameters: {', '.join(missing_params)}")
            return None

        return cls(**{param: parameters[param] for param in required_params})