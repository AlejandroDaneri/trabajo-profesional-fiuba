
from datetime import datetime
import pandas as pd
from binance.client import Client as BinanceProvider

class Binance:
    def __init__(self):
        api_key = "OF6SkzXI0EAcvmMWlkeUKl6YyxYIFU4pN0Bj19gaVYZcgaTt7OImXxEyvoPcDhmk"
        secret_key = "tXay1BDYuSyigxvl27UQIBJbIHADaep8FT7HPO9Mb3vfmcyDkz4keEaHkpm7dcFe"
        self.provider = BinanceProvider(api_key, secret_key, tld='us')

    def binance_get(self, ticker: str, timeframe: str, start=None, end=None, n=1000):
        timeframes = {
            "1M": BinanceProvider.KLINE_INTERVAL_1MINUTE,
            "5M": BinanceProvider.KLINE_INTERVAL_5MINUTE,
            "15M": BinanceProvider.KLINE_INTERVAL_15MINUTE,
            "30M": BinanceProvider.KLINE_INTERVAL_30MINUTE,
            "1H": BinanceProvider.KLINE_INTERVAL_1HOUR,
            "4H": BinanceProvider.KLINE_INTERVAL_4HOUR,
            "1D": BinanceProvider.KLINE_INTERVAL_1DAY,
            "1W": BinanceProvider.KLINE_INTERVAL_1WEEK
        }
        klines = self.provider.get_historical_klines(ticker, timeframes[timeframe], start_str=start, end_str=end, limit=n)
        data = pd.DataFrame(klines, columns = ["Timestamp", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume"," Number of trades"," Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
        data['Date'] = data['Timestamp'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H-%M'))
        data['Close'] =  data['Close'].apply(lambda x : float(x))
        data = data.set_index("Date")
        return data
    
    # example:
    #  ticker: 'BTC'
    #  start: yyyy-mm-dd
    #  start: '2014-01-15'
    #  end: yyyy-mm-dd
    #  end: '2024-03-15'
    def get(self, ticker: str, timeframe: str, start = None, end = None, n = None):
        timeframe_ = timeframe or '1D'

        timeframes = {
            "1M": BinanceProvider.KLINE_INTERVAL_1MINUTE,
            "5M": BinanceProvider.KLINE_INTERVAL_5MINUTE,
            "15M": BinanceProvider.KLINE_INTERVAL_15MINUTE,
            "30M": BinanceProvider.KLINE_INTERVAL_30MINUTE,
            "1H": BinanceProvider.KLINE_INTERVAL_1HOUR,
            "4H": BinanceProvider.KLINE_INTERVAL_4HOUR,
            "1D": BinanceProvider.KLINE_INTERVAL_1DAY,
            "1W": BinanceProvider.KLINE_INTERVAL_1WEEK
        }

        dates = {
            "1M": "%Y-%m-%d %H:%M",
            "5M": "%Y-%m-%d %H:%M",
            "15M": "%Y-%m-%d %H:%M",
            "30M": "%Y-%m-%d %H:%M",
            "1H": "%Y-%m-%d %H",
            "4H": "%Y-%m-%d %H",
            "1D": "%Y-%m-%d"
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
        data['Date'] = data['Date'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime(dates[timeframe_]))
        data['Close'] =  data['Close'].apply(lambda x : float(x))
        data['Open'] =  data['Open'].apply(lambda x : float(x))
        data['High'] =  data['High'].apply(lambda x : float(x))
        data['Low'] =  data['Low'].apply(lambda x : float(x))
        data['Volume'] =  data['Volume'].apply(lambda x : float(x))
        data = data.set_index("Date")
        return data
