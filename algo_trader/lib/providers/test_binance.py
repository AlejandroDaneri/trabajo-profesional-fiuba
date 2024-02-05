from lib.providers.binance import Binance

provider = Binance()

def test_get_latest_n():
    timeframes = ['1M', '5M', '15M', '1H', '4H', '1D']
    for timeframe in timeframes:
        data = provider.get_latest_n('BTCUSDT', timeframe, 1000)
        assert len(data) == 1000
