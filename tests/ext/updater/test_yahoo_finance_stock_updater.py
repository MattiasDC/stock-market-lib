import datetime
import json
from jsonschema import validate
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

	def test_json(self):
		updater = YahooFinanceStockUpdater()
		json_str = updater.to_json()
		self.assertEqual(YahooFinanceStockUpdater.from_json(json_str), updater)
		validate(instance=json.loads(json_str), schema=YahooFinanceStockUpdater.json_schema())

if __name__ == '__main__':
    unittest.main()