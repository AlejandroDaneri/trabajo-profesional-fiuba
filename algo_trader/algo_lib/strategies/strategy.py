from abc import abstractmethod
from typing import List
from algo_lib.actions import Action
from algo_lib.indicators.indicator import Indicator


class Strategy:
    def __init__(self, indicators: List[Indicator]):
        self.indicators = indicators
        self.investment_ratio = 1

    ## consumes all historical data and prepare strategy for predictions
    @abstractmethod
    def train(self, historical_data):
        pass

    ## return the best action based on the latest data.
    @abstractmethod
    def predict(self, new_record) -> Action:
        pass
