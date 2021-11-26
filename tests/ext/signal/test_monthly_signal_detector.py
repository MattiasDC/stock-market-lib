import datetime
import json
from jsonschema import validate
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
		sequence = detector.detect(datetime.date(2000, 1, 2), datetime.date(2000, 1, 2), sm, sequence)
		self.assertFalse(sequence.signals)
		sequence = detector.detect(datetime.date(2000, 2, 1), datetime.date(2000, 2, 1), sm, sequence)
		self.assertEqual(len(sequence.signals), 1)

		sequence = detector.detect(datetime.date(2001, 1, 1), datetime.date(2001, 12, 31), sm, sequence)
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