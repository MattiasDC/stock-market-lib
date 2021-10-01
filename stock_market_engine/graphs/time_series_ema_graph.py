from graphs.time_series_graph import TimeSeriesGraph

class TimeSeriesEMAGraph:
	def __init__(self, time_series):
		self.__graph = TimeSeriesGraph(time_series,
			[("ema20", lambda series: series.ema(20)),
			("ema50", lambda series: series.ema(50))])

	def show(self):
		self.__graph.show()