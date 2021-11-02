import datetime
import unittest
from stock_market_engine.ext.signal import FixedIntervalSignal

class TestFixedIntervalSignal(unittest.TestCase):
						 
	def setUp(self):
		self.date = datetime.date(1970, 2, 2)
		self.name = "test"
		self.signal = FixedIntervalSignal(self.date, self.name)

	def test_name(self):
		self.assertTrue(self.name in self.signal.name) 

	def test_date(self):
		self.assertEqual(self.signal.date, self.date)
		

if __name__ == '__main__':
    unittest.main()