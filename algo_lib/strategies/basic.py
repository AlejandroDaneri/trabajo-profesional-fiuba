from algo_lib.indicators.macd import RSI

class Basic(Strategy):
    def __init__(self,name):
        self.name = "BASIC"
        self.indicators = [new RSI()]
        return
   
    ## consumes all historical data and prepare strategy for predictions
    def train(historical_data):
        return
    
    ## return the best action based on the latest data.
    def predict(latest_data)
        return "BUY"