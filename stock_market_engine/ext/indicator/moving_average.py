import json
import pandas as pd

from stock_market_engine.core.time_series import TimeSeries

class MovingAverage:
	def __init__(self, period):
		self.period = period

	def __call__(self, series : TimeSeries):
		return TimeSeries(f"ma{self.period} {series.name}",
						  pd.concat([series.dates, series.values.rolling(self.period, min_periods=1).mean()],
						  			axis=1,
						  			ignore_index=True))

	def __str__(self):
		return f"MA({self.period})"

	def to_json(self):
		return json.dumps({'period' : self.period})

	@staticmethod
	def from_json(json_str):
		return MovingAverage(**json.loads(json_str))