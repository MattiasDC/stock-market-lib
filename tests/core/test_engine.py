import datetime
import pandas as pd
import unittest
from stock_market_engine.core import Engine
from stock_market_engine.core import OHLC
from stock_market_engine.core import TickerOHLC
from stock_market_engine.core import Ticker
from stock_market_engine.core import Signal
from stock_market_engine.core import SignalDetector
from stock_market_engine.core import StockMarket
from stock_market_engine.core import StockUpdater
from stock_market_engine.common.factory import Factory

class DummyStockMarketUpdater(StockUpdater):
	def __init__(self):
		super().__init__("DummyUpdater")

	def update(self, date, stock_market):
		 ohlc = OHLC(pd.Series([date]), pd.Series([1]), pd.Series([2]), pd.Series([3]), pd.Series([4]))
		 stock_market = stock_market.update_ticker(TickerOHLC(Ticker('SPY'), ohlc))
		 return stock_market

class DummyMonthlySignalDetector(SignalDetector):
	def __init__(self):
		super().__init__("DummyDetector", "DummyDetector")

	def detect(self, date, stock_market, sequence):
		if date.day == 1:
			sequence.add(Signal("DummyDetector", date))

	def update(self, date, stock_market):
		pass

class TestEngine(unittest.TestCase):

	def setUp(self):
		self.spy = Ticker('SPY')
		self.date = datetime.date(2000, 2, 2)
		self.stock_market = StockMarket(self.date, [self.spy])
		self.stock_updater = DummyStockMarketUpdater()
		self.engine = Engine(self.stock_market, self.stock_updater, [DummyMonthlySignalDetector()])

	def test_update(self):
		date = datetime.date(2000, 5, 1)
		self.engine.update(date)
		self.assertEqual(date, self.engine.stock_market.date)
		self.assertEqual(3, len(self.engine.signals.signals))
		last_spy_time_value = self.engine.stock_market.ohlc(self.spy).close.time_values.iloc[-1]
		self.assertEqual(date, last_spy_time_value.date)
		self.assertEqual(4, last_spy_time_value.value)

	def test_json(self):
		factory = Factory()
		factory.register("DummyDetector", lambda _: DummyMonthlySignalDetector())
		factory.register("DummyUpdater", lambda _: DummyStockMarketUpdater())
		from_json = Engine.from_json(self.engine.to_json(), factory, factory)
		self.assertEqual(self.engine.stock_market, from_json.stock_market)
		self.assertEqual(self.engine.signals, from_json.signals)

if __name__ == '__main__':
    unittest.main()