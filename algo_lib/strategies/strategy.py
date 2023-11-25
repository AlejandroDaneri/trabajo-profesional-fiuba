from abc import abstractmethod


class Strategy:
    
    ## consumes all historical data and prepare strategy for predictions
    @abstractmethod
    def train(self,historical_data):
        pass
    
    ## return the best action based on the latest data.
    @abstractmethod
    def predict(self,new_record):
        pass

