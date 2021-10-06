import dateparser
import datetime
import pandas as pd
import unittest
from stock_market_engine.core.ohlc import OHLC

class TestOHLC(unittest.TestCase):

	def setUp(self):
		self.raw_data = pd.read_csv("tests/data/SPY.csv")
		self.ohlc = OHLC(self.raw_data.Date,
						 self.raw_data.Open,
						 self.raw_data.High,
						 self.raw_data.Low,
						 self.raw_data.Close)
						 
	def test_start(self):
		self.assertEqual(dateparser.parse(self.raw_data["Date"].iloc[0]).date(), self.ohlc.start)

	def test_end(self):
		self.assertEqual(dateparser.parse(self.raw_data["Date"].iloc[-1]).date(), self.ohlc.end)

	def test_dates(self):
		self.assertTrue(pd.to_datetime(self.raw_data["Date"]).dt.date.equals(self.ohlc.dates))

	def test_open(self):
		self.assertTrue((self.raw_data["Open"].values == self.ohlc.open.values).all())

	def test_high(self):
		self.assertTrue((self.raw_data["High"].values == self.ohlc.high.values).all())

	def test_loq(self):
		self.assertTrue((self.raw_data["Low"].values == self.ohlc.low.values).all())

	def test_close(self):
		self.assertTrue((self.raw_data["Close"].values == self.ohlc.close.values).all())

	def test_trimmed_start(self):
		trimmed = self.ohlc.trimmed_start(10)
		self.assertEqual(trimmed.end - trimmed.start, datetime.timedelta(days=10))
		self.assertEqual(trimmed.end, self.ohlc.end)
		self.assertEqual(trimmed.start, self.ohlc.end - datetime.timedelta(days=10))

if __name__ == '__main__':
    unittest.main()