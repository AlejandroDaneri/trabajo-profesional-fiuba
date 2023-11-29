from abc import abstractmethod

from algo_lib.actions import Action


class Strategy:
    
    ## consumes all historical data and prepare strategy for predictions
    @abstractmethod
    def train(self,historical_data):
        pass
    
    ## return the best action based on the latest data.
    @abstractmethod
    def predict(self,new_record)->Action:
        pass

