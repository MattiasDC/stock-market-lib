from stock_market_engine.core.time_series import TimeSeries
from stock_market_engine.ext.indicator.moving_average import MovingAverage
import datetime
import pandas as pd
import unittest

class TestMovingAverage(unittest.TestCase):
						 
	def test_ma(self):
		series = TimeSeries("dummy", pd.DataFrame(data=[[datetime.date(2020, 1, 1), 0],
														[datetime.date(2020,1,2), 10],
														[datetime.date(2020,1,3), 10]]))
		ma = MovingAverage(2)
		ma_series = ma(series)
		self.assertEqual(len(ma_series), 3)
		self.assertEqual(ma_series.values.iloc[0], 0)
		self.assertEqual(ma_series.values.iloc[1], 5)
		self.assertEqual(ma_series.values.iloc[2], 10)

if __name__ == '__main__':
    unittest.main()