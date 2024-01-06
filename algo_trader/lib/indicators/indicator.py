from abc import abstractmethod


class Indicator:
    def __init__(self, name):
        self.name = name
        return

    @abstractmethod
    def calculate(self, *args):
        pass
    
    @abstractmethod
    def predict_signal(self, new_record):
        pass

    @abstractmethod
    def calc_buy_signal(self):
        pass

    @abstractmethod
    def calc_sell_signal(self):
        pass
