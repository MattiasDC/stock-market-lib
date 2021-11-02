import datetime
import unittest
from stock_market_engine.core import Signal
from stock_market_engine.core import SignalDetector
from stock_market_engine.core import SignalSequence

class TestSignalDetector(unittest.TestCase):
						 
	def setUp(self):
		self.name = "TestSignal"

	def create(self, date):
		return Signal(self.name, date)

	def test_name(self):
		self.assertEqual(SignalDetector(self.name, self).name, self.name)

	def test_signal(self):
		date = datetime.datetime.now().date()
		signal_sequence = SignalSequence()
		SignalDetector(self.name, self).signal(date, signal_sequence)
		self.assertEqual(len(signal_sequence.signals), 1)
		self.assertEqual(signal_sequence.signals[0].name, self.name)
		self.assertEqual(signal_sequence.signals[0].date, date)

if __name__ == '__main__':
    unittest.main()