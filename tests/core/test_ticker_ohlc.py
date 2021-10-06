import unittest
import pandas as pd
from stock_market_engine.core.ticker_ohlc import TickerOHLC
from stock_market_engine.core.ticker import Ticker
from stock_market_engine.core.ohlc import OHLC

class TestTickerOHLC(unittest.TestCase):
			
	def setUp(self):
		self.ticker = Ticker("Test")
		self.raw_data = pd.read_csv("tests/data/SPY.csv")
		self.ohlc = OHLC(self.raw_data.Date,
						 self.raw_data.Open,
						 self.raw_data.High,
						 self.raw_data.Low,
						 self.raw_data.Close)		 

	def test_ticker(self):
		ticker_ohlc = TickerOHLC(self.ticker, self.ohlc)
		self.assertEqual(ticker_ohlc.ticker, self.ticker)

	def test_ohlc(self):
		ticker_ohlc = TickerOHLC(self.ticker, self.ohlc)
		self.assertEqual(ticker_ohlc.ohlc, self.ohlc)

if __name__ == '__main__':
    unittest.main()