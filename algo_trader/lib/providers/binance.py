
from datetime import datetime
import pandas as pd
from binance.client import Client as BinanceProvider
from lib.constants.timeframe import *

class Binance:
    def __init__(self):
        api_key = "OF6SkzXI0EAcvmMWlkeUKl6YyxYIFU4pN0Bj19gaVYZcgaTt7OImXxEyvoPcDhmk"
        secret_key = "tXay1BDYuSyigxvl27UQIBJbIHADaep8FT7HPO9Mb3vfmcyDkz4keEaHkpm7dcFe"
        self.provider = BinanceProvider(api_key, secret_key, tld='us')
    
    # example:
    #  ticker: 'BTC'
    #  start: yyyy-mm-dd
    #  start: '2014-01-15'
    #  end: yyyy-mm-dd
    #  end: '2024-03-15'
    def get(self, ticker: str, timeframe: str, start = None, end = None, n = None):
        timeframe_ = timeframe or TIMEFRAME_1_DAY

        timeframes = {
            TIMEFRAME_1_MIN: BinanceProvider.KLINE_INTERVAL_1MINUTE,
            TIMEFRAME_5_MIN: BinanceProvider.KLINE_INTERVAL_5MINUTE,
            TIMEFRAME_15_MIN: BinanceProvider.KLINE_INTERVAL_15MINUTE,
            TIMEFRAME_30_MIN: BinanceProvider.KLINE_INTERVAL_30MINUTE,
            TIMEFRAME_1_HOUR: BinanceProvider.KLINE_INTERVAL_1HOUR,
            TIMEFRAME_4_HOUR: BinanceProvider.KLINE_INTERVAL_4HOUR,
            TIMEFRAME_1_DAY: BinanceProvider.KLINE_INTERVAL_1DAY,
            TIMEFRAME_1_WEEK: BinanceProvider.KLINE_INTERVAL_1WEEK
        }

        if n is None:
            start_ = datetime.strptime(start, '%Y-%m-%d')
            start_unix = int(datetime.timestamp(start_)) * 1000

            end_ = datetime.strptime(end, '%Y-%m-%d')
            end_unix = int(datetime.timestamp(end_)) * 1000

            klines = self.provider.get_historical_klines(f"{ticker}USDT", timeframes[timeframe_], start_str=start_unix, end_str=end_unix)
        else:
            klines = self.provider.get_historical_klines(f"{ticker}USDT", timeframes[timeframe_], limit=n)

        data = pd.DataFrame(klines, columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume"," Number of trades"," Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
        data["Timestamp"] = data['Date']
        data['Date'] = data['Date'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime(DATE_FORMAT[timeframe_]))
        data['Close'] =  data['Close'].apply(lambda x : float(x))
        data['Open'] =  data['Open'].apply(lambda x : float(x))
        data['High'] =  data['High'].apply(lambda x : float(x))
        data['Low'] =  data['Low'].apply(lambda x : float(x))
        data['Volume'] =  data['Volume'].apply(lambda x : float(x))
        data = data.set_index("Date")
        return data
