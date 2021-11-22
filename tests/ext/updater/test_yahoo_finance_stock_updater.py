import datetime
import unittest
from stock_market.core import StockMarket
from stock_market.core import Ticker
from stock_market.ext.updater import YahooFinanceStockUpdater

class TestYahooFinanceStockUpdater(unittest.TestCase):
						 
	def test_update(self):
		spy = Ticker('SPY')
		sm = StockMarket(datetime.date(2000, 1, 1), [spy])
		self.assertEqual(sm.ohlc(spy), None)
		sm = YahooFinanceStockUpdater().update(datetime.datetime.now().date(), sm)
		self.assertNotEqual(sm.ohlc(spy), None)

if __name__ == '__main__':
    unittest.main()