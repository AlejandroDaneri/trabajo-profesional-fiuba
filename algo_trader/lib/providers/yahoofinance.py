from lib.constants.timeframe import *
import yfinance as yf

class YahooFinance:
    # example:
    #  ticker: 'BTC'
    #  start: yyyy-mm-dd hh:mm
    #  start: '2014-01-15 12:30'
    #  end: yyyy-mm-dd hh:mm
    #  end: '2024-03-15 14:30'
    def get(self, ticker: str, timeframe: str, start: str, end: str):
        timeframes = {
            TIMEFRAME_1_MIN: '1m',
            TIMEFRAME_5_MIN: '5m',
            TIMEFRAME_15_MIN: '15m',
            TIMEFRAME_1_HOUR: '1h',
            TIMEFRAME_4_HOUR: '4h',
            TIMEFRAME_1_DAY: '1d',
            TIMEFRAME_1_WEEK: '1wk'
        }
        data = yf.download(f'{ticker}-USD', interval=timeframes[timeframe], auto_adjust=True, progress=False, start=start, end=end)
        data['Date'] = data.index
        data.index = data['Date'].apply(lambda x : x.strftime(DATE_FORMAT[timeframe]))
        data.index
        return data
