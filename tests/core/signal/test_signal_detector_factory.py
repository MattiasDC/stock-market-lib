import datetime
import unittest
from stock_market_engine.core.signal.signal_detector_factory import SignalDetectorFactory
from stock_market_engine.ext.signal.fixed_interval_signal import BiMonthlySignalDetector
from stock_market_engine.ext.signal.fixed_interval_signal import MonthlySignalDetector

class TestSignalDetectorFactory(unittest.TestCase):

	def test_create(self):
		self.assertEqual(SignalDetectorFactory().create({"name" : "monthly"}), MonthlySignalDetector())
		self.assertEqual(SignalDetectorFactory().create({"name" : "bimonthly"}), BiMonthlySignalDetector())

if __name__ == '__main__':
    unittest.main()