import datetime
import unittest

from stock_market.core import Signal, SignalDetector, SignalSequence, StockMarket

class TestSignalDetector(unittest.TestCase):
						 
	def setUp(self):
		self.name = "TestSignal"
		self.id = 1

	def test_name(self):
		self.assertEqual(SignalDetector(self.id, self.name).name, self.name)

	def test_identifier(self):
		self.assertEqual(SignalDetector(self.id, self.name).id, self.id)

	def test_is_valid(self):
		start = datetime.date(2000, 1, 1)
		sm = StockMarket(start, [])
		self.assertTrue(SignalDetector(self.id, self.name).is_valid(sm))

if __name__ == '__main__':
    unittest.main()