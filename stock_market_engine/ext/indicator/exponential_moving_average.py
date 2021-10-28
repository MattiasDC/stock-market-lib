from stock_market_engine.core.time_series import TimeSeries
import pandas as pd

class ExponentialMovingAverage:
	def __init__(self, period_length):
		self.period_length = period_length

	def __call__(self, series : TimeSeries):
		return TimeSeries(f"ema{self.period_length} {series.name}",
						  pd.concat([series.dates, series.values.ewm(span=self.period_length).mean()],
						  			axis=1,
						  			ignore_index=True))