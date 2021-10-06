import pandas as pd
import unittest
from stock_market_engine.core.time_series import TimeSeries
from stock_market_engine.graphs.time_series_ema_graph import TimeSeriesEMAGraph

class TestTimeSeriesEMAGraph(unittest.TestCase):

	def setUp(self):
		self.raw_data = pd.read_csv("tests/data/SPY.csv")

	def test_show(self):
		graph = TimeSeriesEMAGraph(TimeSeries("Close",
			self.raw_data[["Date", "Close"]]))
		graph.show()

if __name__ == '__main__':
    unittest.main()