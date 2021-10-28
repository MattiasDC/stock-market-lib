import dateparser
import datetime
import functools
import pandas as pd
import unittest
from stock_market_engine.core.time_series import TimeSeries

class TestTimeSeries(unittest.TestCase):

	def setUp(self):
		self.raw_data = pd.read_csv("tests/data/SPY.csv")
		self.ts = TimeSeries("Close", self.raw_data[["Date", "Close"]])

	def test_name(self):
		self.assertEqual("Close", self.ts.name)

	def test_start(self):
		self.assertEqual(dateparser.parse(self.raw_data["Date"].iloc[0]).date(), self.ts.start)

	def test_end(self):
		self.assertEqual(dateparser.parse(self.raw_data["Date"].iloc[-1]).date(), self.ts.end)

	def test_duration(self):
		self.assertEqual(self.ts.end - self.ts.start, self.ts.duration)

	def test_values(self):
		self.assertTrue(self.raw_data["Close"].equals(self.ts.values))

	def test_dates(self):
		self.assertTrue(pd.to_datetime(self.raw_data["Date"]).dt.date.equals(self.ts.dates))

	def test_time_values(self):
		data = self.raw_data[["Date", "Close"]].copy()
		data.Date = pd.to_datetime(data.Date).dt.date
		self.assertTrue((data.values == self.ts.time_values.values).all())

	def test_ma_normal(self):
		days = 4
		first_non_include_day = self.ts.start + datetime.timedelta(days=20)
		last_day = first_non_include_day + datetime.timedelta(days=days)
		expected_mean = self.ts.time_values[
			(self.ts.time_values.date <= last_day) &
			(self.ts.time_values.date > first_non_include_day)].value.mean()
		calculated_mean = self.ts.ma_at(last_day, days)
		self.assertEqual(expected_mean, calculated_mean)

	def test_ma_begin(self):
		expected_mean = self.ts.values.iloc[0:2].mean()
		calculated_mean = self.ts.ma_at(self.ts.dates.iloc[1], 4)
		self.assertEqual(expected_mean, calculated_mean)

	def test_ma_end(self):
		expected_mean = self.ts.values.iloc[[-1, -2]].mean()
		calculated_mean = self.ts.ma_at(self.ts.dates.iloc[-1], 2)
		self.assertEqual(expected_mean, calculated_mean)

	def test_keep_recent_days(self):
		month_days = 30
		trimmed_series = self.ts.keep_recent_days(month_days)
		self.assertEqual(trimmed_series.duration, datetime.timedelta(days=month_days-1))
		self.assertEqual(trimmed_series.end, self.ts.end)

	def test_eq(self):
		self.assertEqual(self.ts, self.ts)
		self.assertNotEqual(self.ts, 0)

	def test_json(self):
		self.assertEqual(self.ts, TimeSeries.from_json(self.ts.to_json()))

if __name__ == '__main__':
    unittest.main()