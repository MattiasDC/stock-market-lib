import dateparser
import datetime
import functools
import pandas as pd
from pandas.api.types import is_numeric_dtype
import string

class TimeSeries:
	def __init__(self, name, day_data):
		self.__name = name
		self.__day_data = day_data.copy()
		self.__day_data.columns = ["date", "value"]
		self.__day_data.date = pd.to_datetime(self.__day_data.iloc[:,0]).dt.date
		assert(is_numeric_dtype(self.__day_data.value))
		assert(self.start < self.end)

	@property
	def name(self):
		return self.__name

	@property
	def start(self):
		return self.__day_data.date.iloc[0]

	@property
	def end(self):
		return self.__day_data.date.iloc[-1]

	@property
	def duration(self):
		return self.end - self.start

	@property
	def values(self):
		return self.__day_data.value

	@property
	def dates(self):
		return self.__day_data.date
		
	@property
	def time_values(self):
		return self.__day_data

	def ma_at(self, date, days):
		assert(days > 1)
		begin_date = date - datetime.timedelta(days=days-1)
		assert(date <= self.end)
		return self.time_values.loc[
			(self.time_values.date >= begin_date) &
			(self.time_values.date <= date)].value.mean()

	def ema_at(self, date, days):
		assert(days > 1)
		begin_date = date - datetime.timedelta(days=days-1)
		assert(date <= self.end)
		relevant_values = self.time_values.loc[
			(self.time_values.date >= begin_date) &
			(self.time_values.date <= date)].value
		return relevant_values.ewm(span=len(relevant_values)).mean().iloc[-1]

	def ma(self, days):
		return self.values.rolling(days, min_periods=1).mean()

	def ema(self, days):
		return self.values.ewm(span=days).mean()

	"""
	Trims the series at the start of the series to keep \p days
	"""
	def trimmed_start(self, days):
		return TimeSeries(self.name, self.time_values.loc[self.time_values.date >= self.end - datetime.timedelta(days=days)])

def merge_time_series(first, second):
	assert(first.name == second.name)
	assert(first.end + datetime.timedelta(days=1) == second.start)
	return TimeSeries(first.name, pd.concat(first.__day_data, second.__day_data))