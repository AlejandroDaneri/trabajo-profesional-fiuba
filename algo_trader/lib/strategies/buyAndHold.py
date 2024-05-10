from typing import List
from lib.actions import Action
from lib.indicators.indicator import Indicator
from lib.strategies.strategy import Strategy

class BuyAndHold(Strategy):
    def __init__(self, indicators: List[Indicator], timeframe: str, id: str):
        self.name = "BuyAndHold"
        super().__init__([], timeframe, id)
        self.already_buyed = False

    def prepare_data(self, historical_data):
        # No preparation needed for buy and hold strategy
        pass

    def predict(self, new_record) -> Action:
        if not self.already_buyed:
            self.already_buyed = True
            return Action.BUY
        else:
            return Action.HOLD
