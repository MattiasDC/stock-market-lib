import pandas as pd
import unittest
from stock_market_engine.core.time_series import TimeSeries
from stock_market_engine.graphs.time_series_graph import TimeSeriesGraph

class TestTimeSeriesGraph(unittest.TestCase):

	def setUp(self):
		self.raw_data = pd.read_csv("tests/data/SPY.csv")
		self.graph = TimeSeriesGraph(TimeSeries("Close",
			self.raw_data[["Date", "Close"]]),
			[("ma20", lambda series: series.ma(20)), ("ma50", lambda series: series.ma(50))])

	def test_show(self):
		self.graph.show()

if __name__ == '__main__':
    unittest.main()