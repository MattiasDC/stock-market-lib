import datetime
import json
from jsonschema import validate
import pandas as pd
import unittest

from stock_market.core import StockMarket
from stock_market.core import Ticker
from stock_market.core import merge_signals
from stock_market.ext.signal import MonthlySignalDetector
		
class TestMonthlySignalDetector(unittest.TestCase):

	def test_detect(self):
		spy = Ticker('SPY')
		sm = StockMarket(datetime.date(2000, 1, 1), [spy])
		detector = MonthlySignalDetector(1)
		sequence = detector.detect(datetime.date(2000, 1, 2), sm)
		self.assertFalse(sequence.signals)
		sequence = detector.detect(datetime.date(2000, 2, 1), sm)
		self.assertEqual(len(sequence.signals), 1)

		for date in pd.date_range(datetime.date(2001, 1, 1), datetime.date(2001, 12, 31)):
			sequence = merge_signals(sequence, detector.detect(date.date(), sm))
		self.assertEqual(len(sequence.signals), 13)

		for s in sequence.signals:
			self.assertEqual(s.date.day, 1)

	def test_json(self):
		detector = MonthlySignalDetector(1)
		json_str = detector.to_json()
		self.assertEqual(MonthlySignalDetector.from_json(json_str), detector)
		validate(instance=json.loads(json_str), schema=MonthlySignalDetector.json_schema())

if __name__ == '__main__':
    unittest.main()