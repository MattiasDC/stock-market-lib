from .ohlc import OHLC
from .ticker import Ticker
import datetime
import json

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
		if ticker_OHLC.ohlc.end < self.start_date:
			return

		ohlc = ticker_OHLC.ohlc
		if ohlc.start < self.start_date:
			ohlc = ohlc.trimmed_start((ohlc.end - self.start_date).days)
		assert(ohlc.start >= self.start_date)
		self.__ticker_OHLCs[ticker_OHLC.ticker] = ohlc

	@property
	def date(self):
		if not self.__ticker_OHLCs:
			return self.start_date
		max_date = max(map(lambda ohlc: ohlc.end, self.__ticker_OHLCs.values()))
		assert max_date >= self.start_date
		return max_date

	def __repr__(self):
		return f"StockMarket({self.date}, {self.tickers})"

	def __eq__(self, other):
		if not isinstance(other, StockMarket):
			return False 
		if self.start_date != other.start_date:
			return False
		if len(self.tickers) != len(other.tickers):
			return False # fail quickly
		if sorted(self.tickers) != sorted(other.tickers):
			return False
		if self.date != other.date:
			return False # fail quickly
		if len(self.__ticker_OHLCs) != len(other.__ticker_OHLCs):
			return False # fail quickly
		for ticker in self.tickers:
			if self.ohlc(ticker) != other.ohlc(ticker):
				return False
		return True

	def to_json(self):
		return json.dumps({"start_date" : json.dumps(self.start_date, default=datetime.date.isoformat),
						   "tickers": json.dumps([ticker.to_json() for ticker in self.tickers]),
						   "ticker_ohlcs" : json.dumps(self.__ticker_OHLCs)})

	@staticmethod
	def from_json(json_str):
		json_obj = json.loads(json_str)
		sm = StockMarket(datetime.date.fromisoformat(json.loads(json_obj["start_date"])),
						 [Ticker.from_json(ticker) for ticker in json.loads(json_obj["tickers"])])
		sm.__ticker_OHLCs = json.loads(json_obj["ticker_ohlcs"])
		return sm