from lib.providers.binance import Binance
import unittest
from datetime import datetime

provider = Binance()

class BinanceTests(unittest.TestCase):
    def test_get_latest_n(self):
        # test that list length match with n
        timeframes = ['1M', '5M', '15M', '1H', '4H', '1D']
        for timeframe in timeframes:
            data = provider.get_latest_n('BTCUSDT', timeframe, 1000)
            self.assertEqual(len(data), 1000)

    def test_get_latest_n(self):
        # test that open time increment with the interval expected

        to_seconds = {
            '1M': 60 * 1,
            '5M': 60 * 5,
            '15M': 60 * 15,
            '1H': 60 * 60,
            '4H': 60 * 60 * 4,
            '1D': 60 * 60 * 24
        }

        timeframes = ['1M', '5M', '15M', '1H', '4H', '1D']

        for timeframe in timeframes:
            data = provider.get_latest_n('BTCUSDT', timeframe, 1000)

            prev_value = None
            for index, value in (data['Open time'].apply(lambda x : int(x / 1000))).iteritems():
                if prev_value is not None:
                    self.assertEqual(prev_value + to_seconds[timeframe], value)
                prev_value = value


if __name__ == '__main__':
    unittest.main()

