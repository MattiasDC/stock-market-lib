import json
import pandas as pd

from stock_market_engine.core.time_series import TimeSeries

class ExponentialMovingAverage:
	def __init__(self, period):
		self.period = period

	def __call__(self, series : TimeSeries):
		return TimeSeries(f"ema{self.period} {series.name}",
						  pd.concat([series.dates, series.values.ewm(span=self.period).mean()],
						  			axis=1,
						  			ignore_index=True))

	def __eq__(self, other):
		if not isinstance(other, ExponentialMovingAverage):
			return False
		return self.period == other.period

	def __str__(self):
		return f"EMA({self.period})"

	def to_json(self):
		return json.dumps({'period' : self.period})
	
	@staticmethod
	def from_json(json_str):
		return MovingAverage(**json.loads(json_str))