import dateparser
import datetime
import functools
import json
import pandas as pd
from pandas.api.types import is_numeric_dtype
import string

class TimeSeries:
	def __init__(self, name: str, day_data: pd.DataFrame):
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

	"""
	Trims the series at the start of the series to keep \p days
	"""
	def keep_recent_days(self, days):
		return TimeSeries(self.name, self.time_values.loc[self.time_values.date > self.end - datetime.timedelta(days=days)])

	def __eq__(self, other):
		if not isinstance(other, TimeSeries):
			return False
		if self.name != other.name:
			return False
		if not self.time_values.equals(other.time_values):
			return False
		return True

	def __len__(self):
		return len(self.values)

	def __repr__(self):
		if len(self) == 0:
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
	assert first.end < second.start
	return TimeSeries(first.name, pd.concat([first.time_values, second.time_values], ignore_index=True))

def __find_nearest(value, df, find_col, value_col):
    exactmatch = df[df[find_col] == value]
    if not exactmatch.empty:
        return exactmatch.iloc[0][value_col]
    else:
        lowerneighbour_ind = df[df[find_col] < value][find_col].idxmax()
        upperneighbour_ind = df[df[find_col] > value][find_col].idxmin()
        return (df.iloc[lowerneighbour_ind][value_col] + df.iloc[upperneighbour_ind][value_col])/2.0

def make_relative(time_series_list):
	if not time_series_list:
		return []
		
	def take_start(series):
		return series.start
	relative_min = min(time_series_list, key=take_start)
	relative_min_series = relative_min.time_values.copy()
	relative_min_series.value = relative_min_series.value/relative_min_series.iloc[0].value

	relative_time_series_list = []
	for time_series in time_series_list:
		correction_percentage = __find_nearest(time_series.start, relative_min_series, "date", "value")
		relative_time_values = time_series.time_values.copy()
		base_value = relative_time_values.iloc[0].value/correction_percentage
		relative_time_values.value = relative_time_values.value/base_value
		relative_time_series_list.append(TimeSeries(time_series.name + " (rel)", relative_time_values))
	return relative_time_series_list