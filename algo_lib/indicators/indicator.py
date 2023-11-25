from abc import abstractmethod


class Indicator:
    def __init__(self,name,buy_threshold,sell_threshold):
        self.name = name
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        return
    @abstractmethod
    def calculate(self, *args):
        pass

    def get_output(self):
        return self.output
    
    @abstractmethod
    def calc_buy_signal(self):
        pass
