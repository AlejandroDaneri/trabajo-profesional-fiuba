from abc import abstractmethod
from typing import List
from lib.actions import Action
from lib.indicators.indicator import Indicator

class Strategy:
    def __init__(self, indicators: List[Indicator], timeframe: str, id: str):
        self.indicators = indicators
        self.timeframe = timeframe
        self.id = id
        self.investment_ratio = 1

    ## consumes all historical data and prepare strategy for predictions
    @abstractmethod
    def prepare_data(self, historical_data):
        pass

    ## return the best action based on the latest data.
    @abstractmethod
    def predict(self, new_record) -> Action:
        pass
    
    def get_timeframe(self) -> str:
        return self.timeframe
    
    def get_id(self) -> str:
        return self.id
