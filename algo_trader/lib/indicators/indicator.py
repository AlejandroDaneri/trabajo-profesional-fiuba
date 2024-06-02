from abc import abstractmethod
from inspect import signature
import numpy as np
from lib.actions import Action
from typing import get_type_hints

class Indicator:
    def __init__(self, name: str):
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
        sig = signature(cls.__init__)
        required_params = [param for param, param_info in sig.parameters.items() if param != 'self' and param_info.default == param_info.empty]
        
        if parameters is None:
            print(f"Indicator {cls.__name__} does not have parameters")
            return None

        missing_params = [param for param in required_params if param not in parameters]
        if missing_params:
            print(f"Indicator {cls.__name__} is missing required parameters: {', '.join(missing_params)}")
            return None

        return cls(**{param: parameters[param] for param in parameters})
    
    def to_dict(self):
        params = {attr: getattr(self, attr) for attr in self.__dict__ if not attr.startswith('__')}
        return {
            "name": self.__class__.__name__,
            "parameters": params
        }
    
    @classmethod
    def to_dict_class(cls):
        params = {}
        init_params = signature(cls.__init__).parameters.values()

        for param in init_params:
            param_name = param.name
            if (param_name=="self"):  
                continue
            default_value = param.default
            params[param_name] = {
                'type': param.annotation.__name__,
                'default': default_value if default_value is not param.empty else 'required'
            }
        
        return {
            'name': cls.__name__,
            'parameters': params
        }