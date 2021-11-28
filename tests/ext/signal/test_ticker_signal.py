import datetime as dt
import unittest

from stock_market.core import Ticker, Sentiment
from stock_market.ext.signal import TickerSignal

class TestTickerSignal(unittest.TestCase):

	def test_creation(self):
		spy = Ticker("SPY")
		date = dt.date(2021, 1, 1)
		identifier = 1
		signal = TickerSignal(identifier, "test_signal", Sentiment.BULLISH, spy, date)
		self.assertEqual(signal.ticker, spy)
		self.assertEqual(signal.date, date)
		self.assertEqual(signal.id, identifier)

	def test_equal(self):
		spy = Ticker("SPY")
		date = dt.date(2021, 1, 1)
		identifier = 1
		signal = TickerSignal(identifier, "test_signal", Sentiment.BULLISH, spy, date)
		self.assertEqual(signal, signal)
		self.assertNotEqual(signal, TickerSignal(identifier, "test_signal", Sentiment.BULLISH, Ticker("QQQ"), date))
		self.assertNotEqual(signal, TickerSignal(identifier, "test_signal", Sentiment.BULLISH, spy, date+dt.timedelta(days=1)))

if __name__ == '__main__':
    unittest.main()