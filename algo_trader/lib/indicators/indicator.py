from abc import abstractmethod


class Indicator:
    def __init__(self, name):
        self.name = name
        return

    def calculate(self, data, normalize=False):
        if normalize:
            return self.normalize_output()
        return self.output

    @abstractmethod
    def predict_signal(self, new_record):
        pass

    @abstractmethod
    def calc_buy_signals(self):
        pass

    @abstractmethod
    def calc_sell_signals(self):
        pass

    def normalize_output(self):
        mean = self.output.mean()
        std = self.output.std()
        return (self.output - mean) / std

    def generate_signals(self):
        buy_signals = self.calc_buy_signals()
        sell_signals = self.calc_sell_signals()

        return buy_signals + sell_signals
