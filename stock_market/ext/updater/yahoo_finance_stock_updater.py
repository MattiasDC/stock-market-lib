from stock_market.core.ohlc import OHLC, merge_ohlcs
from stock_market.core.stock_updater import StockUpdater
from stock_market.core.ticker_ohlc import TickerOHLC

from utils.logging import get_logger

import datetime
import json
import yahoo_fin.stock_info as yf

logger = get_logger(__name__)

class YahooFinanceStockUpdater(StockUpdater):
	def __init__(self):
		super().__init__("yahoo")

	def __get_period(self, stock_market, ohlc, date):
		return ohlc.end, date

	def __get_ohlc(self, start, end, ticker):
		ticker_hist = None
		try:
			ticker_hist = yf.get_data(ticker.symbol, start_date=start, end_date=end, interval="1d", index_as_date=False)
			ticker_hist = ticker_hist.reset_index()
		except json.decoder.JSONDecodeError:
			logger.warning("Yahoo Finance rate limit encountered!")
			return None
		except AssertionError: # Be flexible in start and end ranges
			return None
		except KeyError: # Occurs when no data could be retrieved for the interval (e.g. only weekend interval, bug in yahoo_fin)
			return None

		if len(ticker_hist.date) == 0:
			return None
		return OHLC(ticker_hist.date,
					ticker_hist.open,
					ticker_hist.high,
					ticker_hist.low,
					ticker_hist.adjclose)


	def __update_ticker(self, date, stock_market, ticker):
		date_inclusive = date + datetime.timedelta(days=1)
		ohlc = stock_market.ohlc(ticker)
		if ohlc is None:
			start = stock_market.start_date
			end = date_inclusive
		else:
			start, end = self.__get_period(stock_market, ohlc, date_inclusive)

		new_ohlc = self.__get_ohlc(start, end, ticker)
		if new_ohlc is not None:
			stock_market = stock_market.update_ticker(TickerOHLC(ticker, merge_ohlcs(ohlc, new_ohlc)))
		return stock_market

	def update(self, date, stock_market):
		for ticker in stock_market.tickers:
			stock_market = self.__update_ticker(date, stock_market, ticker)
		return stock_market

	def __eq__(self, other):
		return isinstance(other, YahooFinanceStockUpdater)

	def to_json(self):
		return json.dumps({})

	@staticmethod
	def from_json(json_str):
		return YahooFinanceStockUpdater()

	@staticmethod
	def json_schema():
		return {"type": "object"}