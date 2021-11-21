import unittest

from stock_market_engine.core import Signal
from stock_market_engine.core import SignalDetector
from stock_market_engine.core import SignalSequence

class TestSignalDetector(unittest.TestCase):
						 
	def setUp(self):
		self.name = "TestSignal"
		self.id = 1

	def test_name(self):
		self.assertEqual(SignalDetector(self.id, self.name).name, self.name)

	def test_identifier(self):
		self.assertEqual(SignalDetector(self.id, self.name).id, self.id)

if __name__ == '__main__':
    unittest.main()