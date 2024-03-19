
from datetime import datetime
import pandas as pd
from binance.client import Client as BinanceProvider
from datetime import date, timedelta
import os
import math

class Cache:
    def __init__(self):
        self.base_path = "/data/cache_binance"

    def lazy_folder_creation(self, ticker: str):
        # verify if pair folder exists
        pair_folder_path = f"{self.base_path}/{ticker}"

        if os.path.isdir(pair_folder_path) is False:
            # create pair folder
            os.makedirs(pair_folder_path)

    def get_month(self, ticker: str, month: date):
        self.lazy_folder_creation(ticker)

        pair_folder_path = f"{self.base_path}/{ticker}"
        # try to get from cache
        try:
            data = pd.read_csv(f'{pair_folder_path}/{ticker}__{month.strftime("%Y-%m")}__1D.csv')
            data = data.set_index("Open")

            return data
        except:
            return None
        
    def get_day(self, ticker: str, timeframe: str, day: date):
        self.lazy_folder_creation(ticker)

        pair_folder_path = f"{self.base_path}/{ticker}"
        # try to get from cache
        try:
            data = pd.read_csv(f'{pair_folder_path}/{ticker}__{str(day)}__{timeframe}.csv')
            data = data.set_index("Open")

            return data
        except:
            return None
    
    def set_month(self, ticker: str, month: date, data):
        # not save on cache non closed month
        today = date.today()
        if month.year == today.year and month.month == today.month:
            return

        pair_folder_path = f"/data/cache_binance/{ticker}"
        data.to_csv(f'{pair_folder_path}/{ticker}__{month.strftime("%Y-%m")}__1D.csv')

    def set_day(self, ticker: str, timeframe: str, day: date, data):
        # not save on cache non closed day
        if day == date.today():
            return

        pair_folder_path = f"/data/cache_binance/{ticker}"
        data.to_csv(f'{pair_folder_path}/{ticker}__{str(day)}__{timeframe}.csv')

class Binance:
    def __init__(self, cache_enabled=False):
        api_key = "OF6SkzXI0EAcvmMWlkeUKl6YyxYIFU4pN0Bj19gaVYZcgaTt7OImXxEyvoPcDhmk"
        secret_key = "tXay1BDYuSyigxvl27UQIBJbIHADaep8FT7HPO9Mb3vfmcyDkz4keEaHkpm7dcFe"
        self.provider = BinanceProvider(api_key, secret_key, tld='us')
        self.cache_enabled = cache_enabled
        if (self.cache_enabled):
            self.cache = Cache()

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
            "1D": "%Y-%m-%d",
            "1M": "%Y-%m-%d %H:%M",
            "5M": "%Y-%m-%d %H:%M",
            "1H": "%Y-%m-%d %H"
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

    # ticker: example BTCUSDT
    # timeframe: example 1H
    # n: example 10000
    def get_latest_n(self, ticker: str, timeframe: str, n: int):

        # this timeframes do not use cache
        if timeframe == "1D":
            
            day = datetime.today() - timedelta(days=n)
            months = set()

            while day <= datetime.today():
                months.add(date(day.year, day.month, 1))
                day = day + timedelta(days=1)

            data = None
            for month_i in sorted(months):
                data_month = self.get_by_month(ticker, month_i)

                if data is None:
                    data = data_month
                else:
                    data = pd.concat([data, data_month])

            
            to_delete = len(data) - n
            return data.iloc[:-to_delete, :]

        # this timeframes uses cache
        if timeframe == "1H" or timeframe == '4H' or timeframe == '1M' or timeframe == '5M' or timeframe == '30M' or timeframe == '15M':

            N_DAYS = {
                "1M": math.ceil(n / (24 * 1 * (60 / 1))) + 1,
                "5M": math.ceil(n / (24 * 1 * (60 / 5))) + 1,
                "15M": math.ceil(n / (24 * 1 * (60 / 15))) + 1,
                "30M": math.ceil(n / (24 * 1 * (60 / 30))) + 1,
                "1H": math.ceil(n / (24 / 1 * (60 / 60))) + 1,
                "4H": math.ceil(n / (24 / 4 * (60 / 60))) + 1
            }

            # build days list required to get n rows
            days = []
            for i in reversed(range(N_DAYS[timeframe])):
                date_i = date.today() - timedelta(days=i)
                days.append(date_i)

            data = None
            for day in days:
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
        return self.binance_get(ticker, timeframe, start_date)
    
    def get_by_month(self, ticker, month: date):

        # try to get from cache
        if (self.cache_enabled):
            data = self.cache.get_month(ticker, month)
            if data is not None:
                return data

        start = str(month)
        end = str(month + timedelta(days=31))
        start_ = datetime.strptime(start, '%Y-%m-%d')
        start__ = int(datetime.timestamp(start_)) * 1000
        end_ = datetime.strptime(end, '%Y-%m-%d')
        end__ = (int(datetime.timestamp(end_)) * 1000)
        data = self.binance_get(ticker, '1D', start__, end__)

        # filter day that not belong to month
        data['Open_'] = data['Date'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H-%M'))
        data['Open_'] = pd.to_datetime(data['Open_'])
        data = data[(data['Open_'].dt.month == month.month)]
        data = data.drop('Open_', axis=1)

        # store response to cache
        if (self.cache_enabled):
            self.cache.set_month(ticker, month, data)
    
        return data

    # ticker: example BTCUSDT
    # timeframe: example 1H
    # day: example 2023-12-08
    def get_by_day(self, ticker: str, timeframe: str, day: date):

        if (self.cache_enabled):
            data = self.cache.get_day(ticker, timeframe, day)
            if data is not None:
                return data

        start = str(day)
        start_ = datetime.strptime(start, '%Y-%m-%d')
        start_unix = int(datetime.timestamp(start_)) * 1000

        end = str(day + timedelta(days=1))
        end_ = datetime.strptime(end, '%Y-%m-%d')
        end_unix = (int(datetime.timestamp(end_)) * 1000)
        
        # to avoid include a row that belong day after
        end_unix = end_unix - 1
        
        data = None
        if timeframe == "1M":
            middle = start_unix + int((end_unix - start_unix) / 2)
            data_1 = self.binance_get(ticker, timeframe, start_unix, end_unix)
            data_2 = self.binance_get(ticker, timeframe, middle, end_unix)
            data = pd.concat([data_1, data_2])
        else:
            data = self.binance_get(ticker, timeframe, start_unix, end_unix)

        if (self.cache_enabled):
            self.cache.set_day(ticker, timeframe, day, data)

        return data
