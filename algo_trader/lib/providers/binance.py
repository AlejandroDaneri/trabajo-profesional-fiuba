
from datetime import datetime
import pandas as pd
from binance.client import Client as BinanceProvider
from datetime import date, timedelta
import os
import math

def cache_get_month(ticker: str, month: date):
    # verify if pair folder exists
    pair_folder_path = f"/data/cache_binance/{ticker}"

    if os.path.isdir(pair_folder_path) is False:
        # create pair folder
        os.makedirs(pair_folder_path)

def cache_get_day(ticker: str, timeframe: str, month: date):
    # verify if pair folder exists
    pair_folder_path = f"/data/cache_binance/{ticker}"

    if os.path.isdir(pair_folder_path) is False:
        # create pair folder
        os.makedirs(pair_folder_path)

    today = date.today()
    if month.year == today.year and month.month == today.month:
        return

    # try to get from cache
    try:
        data = pd.read_csv(f'{pair_folder_path}/{ticker}__{month.strftime("%Y-%m")}__{timeframe}.csv')
        data = data.set_index("Open")

        return data
    except:
        return None
    
def cache_set_month(ticker: str, month: date, data):
    # not save on cache non closed month
    today = date.today()
    if month.year == today.year and month.month == today.month:
        return

    pair_folder_path = f"/data/cache_binance/{ticker}"
    data.to_csv(f'{pair_folder_path}/{ticker}__{month.strftime("%Y-%m")}__1D.csv')

def cache_set_day(ticker: str, timeframe: str, day: date, data):
    # not save on cache non closed day
    if day == date.today():
        return

    pair_folder_path = f"/data/cache_binance/{ticker}"
    data.to_csv(f'{pair_folder_path}/{ticker}__{str(day)}__{timeframe}.csv')

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
        data = pd.DataFrame(klines, columns = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume"," Number of trades"," Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
        data['Open'] = data['Open time'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H-%M'))
        data['Close'] =  data['Close'].apply(lambda x : float(x))
        data = data.set_index("Open")
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
                print(data_month)

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
        data = cache_get_month(ticker, month)
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
        data['Open_'] = data['Open time'].apply(lambda x : datetime.fromtimestamp(x / 1000).strftime('%Y-%m-%d %H-%M'))
        data['Open_'] = pd.to_datetime(data['Open_'])
        data = data[(data['Open_'].dt.month == month.month)]
        data = data.drop('Open_', axis=1)

        # store response to cache
        cache_set_month(ticker, month, data)
    
        return data

    # ticker: example BTCUSDT
    # timeframe: example 1H
    # day: example 2023-12-08
    def get_by_day(self, ticker: str, timeframe: str, day: date):
        data = cache_get(ticker, timeframe, day)
        if data is not None:
            return data

        start = str(day)
        end = str(day + timedelta(days=1))
        start_ = datetime.strptime(start, '%Y-%m-%d')
        start__ = int(datetime.timestamp(start_)) * 1000
        end_ = datetime.strptime(end, '%Y-%m-%d')
        end__ = (int(datetime.timestamp(end_)) * 1000)
        
        # to avoid include a row that belong day after
        end__ = end__ - 1
        
        data = None
        if timeframe == "1M":
            middle = start__ + int((end__ - start__) / 2)
            data_1 = self.binance_get(ticker, timeframe, start__, end__)
            data_2 = self.binance_get(ticker, timeframe, middle, end__)
            data = pd.concat([data_1, data_2])
        else:
            data = self.binance_get(ticker, timeframe, start__, end__)

        cache_set(ticker, timeframe, day, data)

        return data
