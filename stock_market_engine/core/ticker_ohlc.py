
class TickerOHLC:
	def __init__(self, ticker, ohlc):
		self.__ticker = ticker
		self.__ohlc = ohlc

	@property
	def ticker(self):
		return self.__ticker

	@property
	def ohlc(self):
		return self.__ohlc