import datetime
import json
from jsonschema import validate
import pandas as pd
import unittest

from stock_market.core import StockMarket
from stock_market.core import Ticker
from stock_market.core import merge_signals
from stock_market.ext.signal import BiMonthlySignalDetector

class TestBiMonthlySignalDetector(unittest.TestCase):

	def test_detect(self):
		spy = Ticker('SPY')
		sm = StockMarket(datetime.date(2000, 1, 1), [spy])
		detector = BiMonthlySignalDetector(1)
		sequence = detector.detect(datetime.date(2000, 1, 2), sm)
		self.assertFalse(sequence.signals)
		sequence = detector.detect(datetime.date(2000, 1, 15), sm)
		self.assertEqual(len(sequence.signals), 1)
		sequence = merge_signals(sequence, detector.detect(datetime.date(2000, 2, 1), sm))
		self.assertEqual(len(sequence.signals), 2)

		for date in pd.date_range(datetime.date(2001, 1, 1), datetime.date(2001, 12, 31)):
			sequence = merge_signals(sequence, detector.detect(date.date(), sm))
		self.assertEqual(len(sequence.signals), 26)

	def test_json(self):
		detector = BiMonthlySignalDetector(1)
		json_str = detector.to_json()
		self.assertEqual(BiMonthlySignalDetector.from_json(json_str), detector)
		validate(instance=json.loads(json_str), schema=BiMonthlySignalDetector.json_schema())

if __name__ == '__main__':
    unittest.main()