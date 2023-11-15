from abc import abstractmethod


class Indicator:
    def __init__(self,name):
        self.name = name
        return
    @abstractmethod
    def calculate(self, *args):
        pass

    def get_output(self):
        return self.output
