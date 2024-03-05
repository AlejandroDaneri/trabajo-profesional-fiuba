from cryptocmd import CmcScraper
import pandas as pd
from datetime import datetime

class CoinMarketCap:
    # example:
    #  ticker: 'BTC'
    #  start: '20-01-2014'
    def get(self, ticker: str, start: str, end=datetime.now().strftime('%d-%m-%Y')):
        scraper = CmcScraper(ticker, start_date=start, end_date=end)
        headers, data = scraper.get_data()

        data = pd.DataFrame(data, columns=headers)
        data['Open time'] = data['Date'].apply(lambda x : datetime.strptime(x, '%d-%m-%Y').strftime('%Y-%m-%d'))
        data = data.set_index('Open time')
        data = data.sort_index()
        return data
