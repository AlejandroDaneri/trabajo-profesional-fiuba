from cryptocmd import CmcScraper
import pandas as pd
from datetime import datetime

class CoinMarketCap:
    # example:
    #  ticker: 'BTC'
    #  start: '2011-01-01'
    def get(self, ticker: str, start: str):
        scraper = CmcScraper(ticker, start_date=start)
        headers, data = scraper.get_data()

        data = pd.DataFrame(data, columns=headers)
        data['Open time'] = data['Date'].apply(lambda x : datetime.strptime(x, '%d-%m-%Y').strftime('%Y-%m-%d'))
        data = data.set_index('Open time')
        data = data.sort_index()
        return data
