from cryptocmd import CmcScraper
import pandas as pd
from datetime import datetime

class CoinMarketCap:
    # example:
    #  ticker: 'BTC'
    #  start: yyyy-mm-dd
    #  start: '2014-01-15'
    #  end: yyyy-mm-dd
    #  end: '2024-03-15'
    def get(self, ticker: str, start: str, end=None):
        start_date = datetime.strptime(start, '%Y-%m-%d').strftime('%d-%m-%Y')
        end_date = None
        if end is None:
            end_date = datetime.today().strftime('%d-%m-%Y')
        else:
            end_date = datetime.strptime(end, '%Y-%m-%d').strftime('%d-%m-%Y')

        # this API receive format dd-mm-yyyy
        scraper = CmcScraper(ticker, start_date=start_date, end_date=end_date)
        headers, data = scraper.get_data()

        data = pd.DataFrame(data, columns=headers)
        data['Date'] = data['Date'].apply(lambda x : datetime.strptime(x, '%d-%m-%Y').strftime('%Y-%m-%d'))
        data = data.set_index('Date')
        data = data.sort_index()
        return data
