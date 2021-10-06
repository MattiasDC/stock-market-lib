import datetime
import unittest
from stock_market_engine.core.signal.signal import Signal

class TestSignal(unittest.TestCase):
						 
	def setUp(self):
		self.name = "TestSignal"
		self.date = datetime.datetime.now().date()
		self.signal = Signal(self.name, self.date)

	def test_name(self):
		self.assertEqual(self.signal.name, self.name)

	def test_date(self):
		self.assertEqual(self.signal.date, self.date)

if __name__ == '__main__':
    unittest.main()