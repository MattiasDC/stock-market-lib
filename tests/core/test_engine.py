import datetime
import pandas as pd
import unittest
from stock_market_engine.core.engine import Engine
from stock_market_engine.core.ohlc import OHLC
from stock_market_engine.core.ticker_ohlc import TickerOHLC
from stock_market_engine.core.ticker import Ticker
from stock_market_engine.core.signal.signal import Signal
from stock_market_engine.core.signal.signal_detector import SignalDetector
from stock_market_engine.core.stock_market import StockMarket
from stock_market_engine.core.updater.stock_updater import StockUpdater

class DummyStockMarketUpdater(StockUpdater):
	def __init__(self):
		super().__init__("Dummy")

	def update(self, date, stock_market):
		 ohlc = OHLC(pd.Series([date]), pd.Series([1]), pd.Series([2]), pd.Series([3]), pd.Series([4]))
		 stock_market.update_ticker(TickerOHLC(Ticker('SPY'), ohlc))

class DummyMonthlySignalDetector(SignalDetector):
	def __init__(self):
		super().__init__("Dummy")

	def detect(self, date, stock_market, sequence):
		if date.day == 1:
			sequence.add(Signal("Dummy", date))

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

if __name__ == '__main__':
    unittest.main()