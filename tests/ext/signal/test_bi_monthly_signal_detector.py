import datetime
import pandas as pd
import unittest
from stock_market_engine.core import StockMarket
from stock_market_engine.core import Ticker
from stock_market_engine.core import SignalSequence
from stock_market_engine.ext.signal import BiMonthlySignalDetector

class TestBiMonthlySignalDetector(unittest.TestCase):

	def test_detect(self):
		spy = Ticker('SPY')
		sm = StockMarket(datetime.date(2000, 1, 1), [spy])
		sequence = SignalSequence()
		detector = BiMonthlySignalDetector(1)
		sequence = detector.detect(datetime.date(2000, 1, 2), sm, sequence)
		self.assertFalse(sequence.signals)
		sequence = detector.detect(datetime.date(2000, 1, 15), sm, sequence)
		self.assertEqual(len(sequence.signals), 1)
		sequence = detector.detect(datetime.date(2000, 2, 1), sm, sequence)
		self.assertEqual(len(sequence.signals), 2)

		for date in pd.date_range(datetime.date(2001, 1, 1), datetime.date(2001, 12, 31)):
			sequence = detector.detect(date.date(), sm, sequence)
		self.assertEqual(len(sequence.signals), 26)

if __name__ == '__main__':
    unittest.main()