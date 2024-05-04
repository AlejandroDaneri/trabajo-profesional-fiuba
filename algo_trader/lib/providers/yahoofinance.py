import yfinance as yf

class YahooFinance:
    # example:
    #  ticker: 'BTC'
    #  start: yyyy-mm-dd
    #  start: '2014-01-15'
    #  end: yyyy-mm-dd
    #  end: '2024-03-15'
    def get(self, ticker: str, timeframe: str, start: str, end: str):
        timeframes = {
            '1M': '1mo',
            '1w': '1wk',
            '5d': '5d',
            '1d': '1d',
            '4h': '4h',
            '1h': '1h',
            '90m': '90m',
            '30m': '30m',
            '15m': '15m',
            '5m': '5m',
            '2m': '2m',
            '1m': '1m',
        }
        dates = {
            "1m": "%Y-%m-%d %H:%M",
            "5m": "%Y-%m-%d %H:%M",
            "15m": "%Y-%m-%d %H:%M",
            "30m": "%Y-%m-%d %H:%M",
            "1h": "%Y-%m-%d %H",
            "4h": "%Y-%m-%d %H",
            "1d": "%Y-%m-%d"
        }
        data = yf.download(f'{ticker}-USD',interval=timeframes[timeframe], auto_adjust=True, progress=False, start=start, end=end)
        data['Date'] = data.index
        data.index = data['Date'].apply(lambda x : x.strftime(dates[timeframe]))
        data.index
        return data
