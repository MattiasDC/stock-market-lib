import datetime
import unittest
from stock_market_engine.common.factory import Factory
from stock_market_engine.ext.signal.fixed_interval_signal import BiMonthlySignalDetector
from stock_market_engine.ext.signal.fixed_interval_signal import MonthlySignalDetector
from stock_market_engine.ext.signal.register import register_signal_detector_factories

class TestFactory(unittest.TestCase):

	def test_create(self):
		factory = Factory()
		register_signal_detector_factories(factory)
		self.assertEqual(factory.create({"name" : "monthly"}), MonthlySignalDetector())
		self.assertEqual(factory.create({"name" : "bimonthly"}), BiMonthlySignalDetector())

	def test_register(self):
		factory = Factory()
		factory.register("m", lambda _: MonthlySignalDetector())
		self.assertEqual(factory.create({"name" : "m"}), MonthlySignalDetector())

if __name__ == '__main__':
    unittest.main()