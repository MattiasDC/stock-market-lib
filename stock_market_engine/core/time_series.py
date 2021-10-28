import dateparser
import datetime
import functools
import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import string

class TimeSeries:
	def __init__(self, name, day_data):
		self.__name = name
		self.__day_data = day_data.copy()
		self.__day_data.columns = ["date", "value"]
		self.__day_data.date = pd.to_datetime(self.__day_data.iloc[:,0]).dt.date
		assert is_numeric_dtype(self.__day_data.value)
		assert self.start <= self.end

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
		return TimeSeries(f"ma{days} {self.name}", pd.concat([self.dates, self.values.rolling(days, min_periods=1).mean()], axis=1, ignore_index=True))

	def ema(self, days):
		return TimeSeries(f"ema{days} {self.name}", pd.concat([self.dates, self.values.ewm(span=days).mean()], axis=1, ignore_index=True))

	"""
	Trims the series at the start of the series to keep \p days
	"""
	def trimmed_start(self, days):
		return TimeSeries(self.name, self.time_values.loc[self.time_values.date > self.end - datetime.timedelta(days=days)])

	def __eq__(self, other):
		if not isinstance(other, TimeSeries):
			return False
		if self.name != other.name:
			return False
		if not self.time_values.equals(other.time_values):
			return False
		return True

	def __repr__(self):
		if len(self.values) == 0:
			return f"TimeSeries({self.name})"
		return f"TimeSeries({self.name}, {self.dates.iloc[-1]})"

	def to_json(self):
		return json.dumps({"name" : self.name,
						  "day_data" : self.time_values.to_json()})
	@staticmethod
	def from_json(json_str):
		dict_obj = json.loads(json_str)
		return TimeSeries(dict_obj["name"], pd.read_json(dict_obj["day_data"]))

def merge_time_series(first, second):
	assert first.name == second.name
	assert (first.end + datetime.timedelta(days=1) == second.start) or (second.start.weekday() == 0 and second.start > first.end)
	return TimeSeries(first.name, pd.concat([first.time_values, second.time_values], ignore_index=True))