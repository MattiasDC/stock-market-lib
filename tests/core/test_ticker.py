import unittest
from stock_market_engine.core.ticker import Ticker

class TestTicker(unittest.TestCase):
						 
	def test_symbol(self):
		self.assertEqual(Ticker("Test").symbol, "Test")

if __name__ == '__main__':
    unittest.main()