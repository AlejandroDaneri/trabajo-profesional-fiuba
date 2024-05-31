
import yfinance as yf

def get_data(ticker, data_from, data_to, timeframe):
    data = yf.download(ticker, interval=timeframe, auto_adjust=True, progress=False, start=data_from, end=data_to)
    return data
