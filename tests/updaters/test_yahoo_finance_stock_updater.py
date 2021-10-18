import datetime
import unittest
from stock_market_engine.core.stock_market import StockMarket
from stock_market_engine.core.ticker import Ticker
from stock_market_engine.updaters.yahoo_finance_stock_updater import YahooFinanceStockUpdater

class TestYahooFinanceStockUpdater(unittest.TestCase):
						 
	def test_update(self):
		spy = Ticker('SPY')
		sm = StockMarket(datetime.date(2000, 1, 1), [spy])
		self.assertEqual(sm.ohlc(spy), None)
		YahooFinanceStockUpdater().update(datetime.datetime.now().date(), sm)
		self.assertNotEqual(sm.ohlc(spy), None)

if __name__ == '__main__':
    unittest.main()