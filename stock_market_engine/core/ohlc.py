from .time_series import TimeSeries, merge_time_series
import datetime
import pandas as pd

class OHLC:
	def __init__(self, dates, open, high, low, close):
		self.__dates = pd.to_datetime(dates).dt.date
		self.__open = TimeSeries("Open", pd.concat([self.dates, open], axis=1))
		self.__high = TimeSeries("High", pd.concat([self.dates, high], axis=1))
		self.__low = TimeSeries("Low", pd.concat([self.dates, low], axis=1))
		self.__close = TimeSeries("Close", pd.concat([self.dates, close], axis=1))

	@property
	def start(self):
		return self.__dates.iloc[0]

	@property
	def end(self):
		return self.__dates.iloc[-1]

	@property
	def dates(self):
		return self.__dates

	@property
	def open(self):
		return self.__open

	@property
	def high(self):
		return self.__high

	@property
	def low(self):
		return self.__low

	@property
	def close(self):
		return self.__close

def merge_ohlcs(first, second):
	if first is None:
		return second
	assert(second is not None)
	assert(first.end + datetime.timedelta(days=1) == second.start)
	return OHLC(pd.concat([first.dates, second.dates]),
				merge_time_series(first.open, second.open),
				merge_time_series(first.high, second.high),
				merge_time_series(first.low, second.low),
				merge_time_series(first.close, second.close))