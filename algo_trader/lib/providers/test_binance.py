from lib.providers.binance import Binance
import unittest
from datetime import datetime

provider = Binance()

class BinanceTests(unittest.TestCase):
    def test_get_using_n(self):
        # test that list length match with n
        # timeframes = ['1M', '5M', '15M', '1H', '4H', '1D']
        timeframes = ['1M', '5M', '15M', '1H', '4H', '1D']
        for timeframe in timeframes:
            data = provider.get('BTC', timeframe, n=1000)
            self.assertEqual(len(data), 1000)
    
    def test_get_using_start_end(self):
        # test that list begin with the start date
        start = '2024-01-01'
        end = '2024-02-01'
        data = provider.get('BTC', '1D', start=start, end=end)
        self.assertEqual(data.index[0], start)
        self.assertEqual(data.index[-1], end)

if __name__ == '__main__':
    unittest.main()

