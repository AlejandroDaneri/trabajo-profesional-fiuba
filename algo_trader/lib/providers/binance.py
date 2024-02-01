
from datetime import datetime
import pandas as pd
from binance.client import Client as BinanceProvider
from datetime import date, timedelta
import os

class Binance:
    def __init__(self):
        api_key = "OF6SkzXI0EAcvmMWlkeUKl6YyxYIFU4pN0Bj19gaVYZcgaTt7OImXxEyvoPcDhmk"
        secret_key = "tXay1BDYuSyigxvl27UQIBJbIHADaep8FT7HPO9Mb3vfmcyDkz4keEaHkpm7dcFe"
        self.provider = BinanceProvider(api_key, secret_key, tld='us')

    # ticker: example BTCUSDT
    def get_latest_n(self, ticker: str, timeframe: str, n: int):

        # verify if pair folder exists
        pair_folder_path = f"lib/providers/data/{ticker}"
        if os.path.isdir(pair_folder_path) is False:
            # create pair folder
            os.makedirs(pair_folder_path)

        if timeframe == "1H":
            # build days list required to get n rows
            days = []
            for i in reversed(range((n % 24))):
                date_i = date.today() - timedelta(days=i)
                days.append(date_i)

            data = None
            for day in days:
                # voy a buscar al archivo, sino esta voy a binance
                filepath = f"{pair_folder_path}/{ticker}__{day}__{timeframe}"
                if os.path.isfile(filepath):
                    print("El archivo existe.")
                else:
                    data_day = self.get_by_day(ticker, timeframe, day)
                    if data is None:
                        data = data_day
                    else:
                        data = pd.concat([data, data_day])

        to_delete = len(data) - n
        return data.iloc[:-to_delete, :]

    # ticker: example BTCUSDT
    # timeframe: example 1H
    # start_date: example 2023-12-08
    def get_from(self, ticker: str, timeframe: str, start_date: str):
        timeframes = {
            "1M": BinanceProvider.KLINE_INTERVAL_1MINUTE,
            "1H": BinanceProvider.KLINE_INTERVAL_1HOUR,
            "1D": BinanceProvider.KLINE_INTERVAL_1DAY
        }
        start_date_ = datetime.strptime(start_date, '%Y-%m-%d')
        start_date__ = int(datetime.timestamp(start_date_)) * 1000
        klines = self.provider.get_historical_klines(ticker, timeframes[timeframe], start_date__)
        data = pd.DataFrame(klines, columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume"," Number of trades"," Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
        data['Open'] = data['Open time'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H-%M'))
        data['Close'] =  data['Close'].apply(lambda x : float(x))
        data = data.set_index("Open")
        return data
    
    # ticker: example BTCUSDT
    # timeframe: example 1H
    # day: example 2023-12-08
    def get_by_day(self, ticker: str, timeframe: str, day: date):
        timeframes = {
            "1M": BinanceProvider.KLINE_INTERVAL_1MINUTE,
            "1H": BinanceProvider.KLINE_INTERVAL_1HOUR,
            "1D": BinanceProvider.KLINE_INTERVAL_1DAY
        }
        start = str(day)
        end = str(day + timedelta(days=1))
        start_ = datetime.strptime(start, '%Y-%m-%d')
        start__ = int(datetime.timestamp(start_)) * 1000
        end_ = datetime.strptime(end, '%Y-%m-%d')
        end__ = int(datetime.timestamp(end_)) * 1000
        klines = self.provider.get_historical_klines(ticker, timeframes[timeframe], start_str=start__, end_str=end__)
        data = pd.DataFrame(klines, columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume"," Number of trades"," Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
        data['Open'] = data['Open time'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H-%M'))
        data['Close'] =  data['Close'].apply(lambda x : float(x))
        data = data.set_index("Open")
        data = data[:-1]
        return data

