import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

class TimeSeriesGraph:
	def __init__(self, time_series, indicators):
		self.__time_series = time_series
		self.__indicators = indicators

	def show(self):
		fig = plt.figure(self.__time_series.name)

		x = pd.to_datetime(self.__time_series.dates)

		columns = ["date", "value"]
		series = [self.__time_series.time_values]
		for name, indicatorFunction in self.__indicators:
			assert(name not in columns)
			columns.append(name)
			series.append(indicatorFunction(self.__time_series))
		values_and_ma = pd.concat(series, axis=1)
		values_and_ma.columns = columns
		lp = px.line(pd.melt(values_and_ma,
						  	["date"],
						  	value_name="val"),
					x="date",
					y="val",
					color="variable")
		lp.show()