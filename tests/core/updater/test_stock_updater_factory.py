import datetime
import unittest
from stock_market_engine.core.updater.stock_updater_factory import StockUpdaterFactory
from stock_market_engine.ext.updater.yahoo_finance_stock_updater import YahooFinanceStockUpdater

class TestStockUpdaterFactory(unittest.TestCase):

	def test_create(self):
		self.assertEqual(StockUpdaterFactory().create("yahoo"), YahooFinanceStockUpdater())

if __name__ == '__main__':
    unittest.main()