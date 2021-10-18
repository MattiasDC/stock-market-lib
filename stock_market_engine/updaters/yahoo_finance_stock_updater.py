from stock_market_engine.core.ohlc import OHLC, merge_ohlcs
from stock_market_engine.core.stock_updater import StockUpdater
from stock_market_engine.core.ticker_ohlc import TickerOHLC
import datetime
import yfinance as yf

class YahooFinanceStockUpdater(StockUpdater):
	def __init__(self):
		super().__init__("Yahoo Finance stock updater")

	def __get_period(self, stock_market, ohlc):
		start = ohlc.end + datetime.timedelta(days=1)
		end = datetime.datetime.now().date()
		return start, end

	def __get_ohlc(self, start, end, ticker):
		yticker = yf.Ticker(ticker.symbol)
		ticker_hist = yticker.history(start=start, end=end, interval="1d")
		ticker_hist = ticker_hist.reset_index()
		return OHLC(ticker_hist.Date,
					ticker_hist.Open,
					ticker_hist.High,
					ticker_hist.Low,
					ticker_hist.Close)

	def update(self, date, stock_market):
		for ticker in stock_market.tickers:
			ohlc = stock_market.ohlc(ticker)
			if ohlc is None:
				start = datetime.date(1970, 1, 1)
				end = datetime.datetime.now().date()
			else:
				start, end = self.__get_period(stock_market, ohlc)
			
			if start == end:
				continue
			assert(start < end)
			new_ohlc = self.__get_ohlc(start, end, ticker)
			stock_market.update_ticker(TickerOHLC(ticker, merge_ohlcs(ohlc, new_ohlc)))