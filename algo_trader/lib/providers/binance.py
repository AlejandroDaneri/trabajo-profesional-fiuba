
from datetime import datetime
import pandas as pd
from binance.client import Client as BinanceProvider

class Binance:
    def __init__(self):
        api_key = "OF6SkzXI0EAcvmMWlkeUKl6YyxYIFU4pN0Bj19gaVYZcgaTt7OImXxEyvoPcDhmk"
        secret_key = "tXay1BDYuSyigxvl27UQIBJbIHADaep8FT7HPO9Mb3vfmcyDkz4keEaHkpm7dcFe"
        self.provider = BinanceProvider(api_key, secret_key, tld='us')

    # ticker: example BTCUSDT
    def get_latest_n(self, ticker: str, timeframe: str, n: int):
        timeframes = {
            "1M": BinanceProvider.KLINE_INTERVAL_1MINUTE,
            "1H": BinanceProvider.KLINE_INTERVAL_1HOUR,
            "1D": BinanceProvider.KLINE_INTERVAL_1DAY
        }
        klines = self.provider.get_historical_klines(ticker, timeframes[timeframe], limit=n)
        data = pd.DataFrame(klines, columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume"," Number of trades"," Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
        data['Open'] = data['Open time'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H-%M'))
        data['Close'] =  data['Close'].apply(lambda x : float(x))
        data = data.set_index("Open")
        return data

    # ticker: example BTCUSDT
    # start_date: 2023-12-08
    def get_data_from(self, ticker: str, start_date: str):
        start_date_ = datetime.strptime(start_date, '%Y-%m-%d')
        start_date__ = int(datetime.timestamp(start_date_)) * 1000
        klines = self.provider.get_historical_klines(ticker, BinanceProvider.KLINE_INTERVAL_1MINUTE, start_date__)
        data = pd.DataFrame(klines, columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume"," Number of trades"," Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
        data['Open'] = data['Open time'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H-%M'))
        data['Close'] =  data['Close'].apply(lambda x : float(x))
        data = data.set_index("Open")
        return data
