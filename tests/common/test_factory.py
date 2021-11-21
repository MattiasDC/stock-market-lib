import datetime
import json
import unittest

from stock_market_engine.common.factory import Factory
from stock_market_engine.ext.signal.fixed_interval_signal import BiMonthlySignalDetector
from stock_market_engine.ext.signal.fixed_interval_signal import MonthlySignalDetector
from stock_market_engine.ext.signal.register import register_signal_detector_factories

class TestFactory(unittest.TestCase):

	def test_create(self):
		factory = Factory()
		register_signal_detector_factories(factory)
		self.assertEqual(factory.create("monthly", json.dumps({"id" : 1})), MonthlySignalDetector(1))
		self.assertEqual(factory.create("bimonthly", json.dumps({"id" : 1})), BiMonthlySignalDetector(1))

	def test_register(self):
		factory = Factory()
		factory.register("m", MonthlySignalDetector.from_json)
		self.assertEqual(factory.create("m", json.dumps({"id" : 1})), MonthlySignalDetector(1))

if __name__ == '__main__':
    unittest.main()