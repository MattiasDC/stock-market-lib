import datetime
import pandas as pd
import unittest
from stock_market.core import StockMarket
from stock_market.core import Ticker
from stock_market.core import SignalSequence
from stock_market.ext.signal import MonthlySignalDetector
		
class TestMonthlySignalDetector(unittest.TestCase):

	def test_detect(self):
		spy = Ticker('SPY')
		sm = StockMarket(datetime.date(2000, 1, 1), [spy])
		sequence = SignalSequence()
		detector = MonthlySignalDetector(1)
		sequence = detector.detect(datetime.date(2000, 1, 2), sm, sequence)
		self.assertFalse(sequence.signals)
		sequence = detector.detect(datetime.date(2000, 2, 1), sm, sequence)
		self.assertEqual(len(sequence.signals), 1)

		for date in pd.date_range(datetime.date(2001, 1, 1), datetime.date(2001, 12, 31)):
			sequence = detector.detect(date.date(), sm, sequence)
		self.assertEqual(len(sequence.signals), 13)

		for s in sequence.signals:
			self.assertEqual(s.date.day, 1)

if __name__ == '__main__':
    unittest.main()