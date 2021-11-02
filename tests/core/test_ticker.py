import unittest
from stock_market_engine.core import Ticker

class TestTicker(unittest.TestCase):
						 
	def test_symbol(self):
		self.assertEqual(Ticker("Test").symbol, "Test")

	def test_eq(self):
		self.assertEqual(Ticker("T"), Ticker("T"))
		self.assertNotEqual(Ticker("A"), Ticker("T"))
		self.assertNotEqual(Ticker("A"), 0)

	def test_json(self):
		self.assertEqual(Ticker("T"), Ticker.from_json(Ticker("T").to_json()))

if __name__ == '__main__':
    unittest.main()