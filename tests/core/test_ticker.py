import unittest
from stock_market_engine.core.ticker import Ticker

class TestTicker(unittest.TestCase):
						 
	def test_symbol(self):
		self.assertEqual(Ticker("Test").symbol, "Test")

	def test_eq(self):
		self.assertEqual(Ticker("T"), Ticker("T"))
		self.assertNotEqual(Ticker("A"), Ticker("T"))

if __name__ == '__main__':
    unittest.main()