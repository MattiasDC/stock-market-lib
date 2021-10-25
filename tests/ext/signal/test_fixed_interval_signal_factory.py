import datetime
import unittest
from stock_market_engine.ext.signal.fixed_interval_signal import FixedIntervalSignalFactory

class TestFixedIntervalSignalFactory(unittest.TestCase):
						 
	def setUp(self):
		self.date = datetime.date(1970, 2, 2)
		self.name = "test"

	def test_create(self):
		factory = FixedIntervalSignalFactory(self.name)
		signal = factory.create(self.date)
		self.assertTrue(self.name in signal.name) 
		self.assertEqual(signal.date, self.date)

if __name__ == '__main__':
    unittest.main()