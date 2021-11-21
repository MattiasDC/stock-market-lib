import datetime
import unittest

from stock_market_engine.core import Signal

class TestSignal(unittest.TestCase):
						 
	def setUp(self):
		self.name = "TestSignal"
		self.id = 1
		self.date = datetime.datetime.now().date()
		self.signal = Signal(self.id, self.name, self.date)

	def test_name(self):
		self.assertEqual(self.signal.name, self.name)

	def test_id(self):
		self.assertEqual(self.signal.id, self.id)

	def test_date(self):
		self.assertEqual(self.signal.date, self.date)

	def test_eq(self):
		self.assertEqual(self.signal, self.signal)
		self.assertNotEqual(self.signal, 0)

	def test_json(self):
		self.assertEqual(self.signal, Signal.from_json(self.signal.to_json()))

if __name__ == '__main__':
    unittest.main()