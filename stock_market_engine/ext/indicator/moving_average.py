from stock_market_engine.core.time_series import TimeSeries
import pandas as pd

class MovingAverage:
	def __init__(self, period_length):
		self.period_length = period_length

	def __call__(self, series : TimeSeries):
		return TimeSeries(f"ma{self.period_length} {series.name}",
						  pd.concat([series.dates, series.values.rolling(self.period_length, min_periods=1).mean()],
						  			axis=1,
						  			ignore_index=True))