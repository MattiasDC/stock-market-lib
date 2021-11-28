from stock_market.core import TimeSeries
from stock_market.ext.indicator import Identity
import datetime
import pandas as pd
import unittest

class TestIdentity(unittest.TestCase):
						 
	def test_ema(self):
		series = TimeSeries("dummy", pd.DataFrame(data=[[datetime.date(2020, 1, 1), 0],
														[datetime.date(2020,1,2), 10],
														[datetime.date(2020,1,3), 10]]))
		identity = Identity()
		identity_series = identity(series)
		self.assertEqual(identity_series, series)

if __name__ == '__main__':
    unittest.main()