from lib.strategies.basic import Basic
from lib.indicators.rsi import RSI
from lib.indicators.crossing import Crossing
from datetime import datetime
import pandas as pd
from cryptocmd import CmcScraper

# get BTC prices using CMC provider
scraper = CmcScraper('BTC', start_date='2011-01-01')
headers, data = scraper.get_data()
data = pd.DataFrame(data, columns=headers)
data['Open'] = data['Date'].apply(lambda x : datetime.strptime(x, '%d-%m-%Y').strftime('%Y-%m-%d')) 
data = data.set_index('Open')
data = data.sort_index()
data

# creates indicators and strategy 
rsi = RSI(40, 60, 14)
basic_strategy = Basic(indicators=[rsi])

# backtesting
trades = basic_strategy.backtest(data)
print(trades)
