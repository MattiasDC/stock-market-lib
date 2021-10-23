from .ohlc import OHLC

class StockMarket:
	def __init__(self, start_date, tickers):
		assert(tickers)
		self.__start_date = start_date
		self.__tickers = tickers
		self.__ticker_OHLCs = {}

	@property
	def start_date(self):
		return self.__start_date

	@property
	def tickers(self):
		return self.__tickers

	def ohlc(self, ticker):
		return self.__ticker_OHLCs.get(ticker)

	def update_ticker(self, ticker_OHLC):
		assert(ticker_OHLC.ticker in self.tickers)
		assert(ticker_OHLC.ohlc.end > self.start_date)

		ohlc = ticker_OHLC.ohlc
		if ohlc.start < self.start_date:
			ohlc = ohlc.trimmed_start((ohlc.end - self.start_date).days)
		assert(ohlc.start >= self.start_date)
		self.__ticker_OHLCs[ticker_OHLC.ticker] = ohlc

	@property
	def date(self):
		if not self.__ticker_OHLCs:
			return self.start_date
		return max(map(lambda ohlc: ohlc.end, self.__ticker_OHLCs.values()))

	def __repr__(self):
		return f"StockMarket({self.date}, {self.tickers})"

	def __str__(self):
		return self.__repr__()