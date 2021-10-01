from .ohlc import OHLC

class StockMarket:
	def __init__(self, tickers):
		self.__tickers = tickers
		self.__ticker_OHLCs = {}

	@property
	def tickers(self):
		return self.__tickers

	def ohlc(self, ticker):
		return self.__tickerOHLCs.get(ticker, OHLC())

	def update_ticker(self, ticker_OHLC):
		assert(ticker_OHLC.ticker in self.tickers)
		self.__ticker_OHLCs[ticker_OHLC.ticker] = ticker_OHLC

	def update_tickers(self, ticker_OHLCs):
		for ticker_OHLC in ticker_OHLCs:
			self.update_ticker(ticker_OHLC)