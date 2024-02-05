import unittest
from lib.providers.binance import Binance

provider = Binance()

class TestGetLatestN(unittest.TestCase):
    def test_timeframe_1h(self):
        data = provider.get_latest_n('BTCUSDT', '1H', 1000)
        self.assertEqual(len(data), 1000)

    def test_timeframe_1m(self):
        data = provider.get_latest_n('BTCUSDT', '1M', 1000)
        self.assertEqual(len(data), 1000)

    def test_timeframe_5m(self):
        data = provider.get_latest_n('BTCUSDT', '5M', 1000)
        self.assertEqual(len(data), 1000)

    def test_timeframe_15m(self):
        data = provider.get_latest_n('BTCUSDT', '15M', 1000)
        self.assertEqual(len(data), 1000)

    def test_timeframe_1h(self):
        data = provider.get_latest_n('BTCUSDT', '1H', 1000)
        self.assertEqual(len(data), 1000)

    def test_timeframe_4h(self):
        data = provider.get_latest_n('BTCUSDT', '4H', 1000)
        self.assertEqual(len(data), 1000)

    def test_timeframe_1d(self):
        data = provider.get_latest_n('BTCUSDT', '1D', 1000)
        self.assertEqual(len(data), 1000)

# Running the tests
if __name__ == '__main__':
    unittest.main()