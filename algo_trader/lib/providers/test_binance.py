from lib.providers.binance import Binance
import logging
provider = Binance()
logging.getLogger().info("boo %s", "arg")
def test_timeframe_1h():
    data = provider.get_latest_n('BTCUSDT', '1H', 1000)
    assert len(data) == 1000

def test_timeframe_1m():
    data = provider.get_latest_n('BTCUSDT', '1M', 1000)
    assert len(data) == 1000

def test_timeframe_5m():
    data = provider.get_latest_n('BTCUSDT', '5M', 1000)
    assert len(data) == 1000

def test_timeframe_15m():
    data = provider.get_latest_n('BTCUSDT', '15M', 1000)
    assert len(data) == 1000

def test_timeframe_1h():
    data = provider.get_latest_n('BTCUSDT', '1H', 1000)
    assert len(data) == 1000

def test_timeframe_4h():
    data = provider.get_latest_n('BTCUSDT', '4H', 1000)
    assert len(data) == 1000

def test_timeframe_1d():
    data = provider.get_latest_n('BTCUSDT', '1D', 1000)
    assert len(data) == 1000
    
def test_timeframe_1d_2000():
    print("hola")
    data = provider.get_latest_n('BTCUSDT', '1D', 2000)
    assert len(data) == 2000