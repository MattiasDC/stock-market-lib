from .ohlc import OHLC

class StockMarket:
	def __init__(self, tickers):
		self.__tickers = tickers
		self.__ticker_OHLCs = {}

	@property
	def tickers(self):
		return self.__tickers

	def ohlc(self, ticker):
		return self.__ticker_OHLCs.get(ticker)

	def update_ticker(self, ticker_OHLC):
		assert(ticker_OHLC.ticker in self.tickers)
		self.__ticker_OHLCs[ticker_OHLC.ticker] = ticker_OHLC.ohlc

	@property
	def date(self):
		return max(map(lambda _, th: th.ohlc.end, self.__ticker_OHLCs))