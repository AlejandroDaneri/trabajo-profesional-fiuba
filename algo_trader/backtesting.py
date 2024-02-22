from lib.strategies.basic import Basic
from lib.indicators.rsi import RSI
from lib.indicators.crossing import Crossing
from lib.providers.coinmarketcap import CoinMarketCap

# get BTC prices using CMC provider
provider = CoinMarketCap()
data = provider.get('BTC', start='2011-01-01')

# creates indicators and strategy 
rsi = RSI(40, 60, 14)
basic_strategy = Basic(indicators=[rsi])

# backtesting
trades = basic_strategy.backtest(data)
print(trades)
