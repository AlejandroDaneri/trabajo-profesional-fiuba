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
            '1m': '1m',
            '5m': '5m',
            '15m': '15m',
            '30m': '30m',
            '45m': '45m',
            '90m': '90m',
            '1h': '1h',
            '4h': '4h',
            '1d': '1d',
            '1w': '1wk',
            '1M': '1mo'
        }
        dates = {
            "1m": "%Y-%m-%d %H:%M",
            "5m": "%Y-%m-%d %H:%M",
            "15m": "%Y-%m-%d %H:%M",
            "30m": "%Y-%m-%d %H:%M",
            "45m": "%Y-%m-%d %H:%M",
            "1h": "%Y-%m-%d %H",
            "4h": "%Y-%m-%d %H",
            "1d": "%Y-%m-%d",
            '1w': "%Y-%m-%d",
            '1M': "%Y-%m-%d"
        }
        data = yf.download(f'{ticker}-USD',interval=timeframes[timeframe], auto_adjust=True, progress=False, start=start, end=end)
        data['Date'] = data.index
        data.index = data['Date'].apply(lambda x : x.strftime(dates[timeframe]))
        data.index
        return data
