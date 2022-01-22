import datetime as dt
import unittest

import dateparser
import pandas as pd

from stock_market.core import TimeSeries
from stock_market.core.time_series import make_relative


class TestTimeSeries(unittest.TestCase):
    def setUp(self):
        self.raw_data = pd.read_csv("tests/data/SPY.csv")
        self.ts = TimeSeries("Close", self.raw_data[["Date", "Close"]])

    def test_name(self):
        self.assertEqual("Close", self.ts.name)

    def test_start(self):
        self.assertEqual(
            dateparser.parse(self.raw_data["Date"].iloc[0]).date(), self.ts.start
        )

    def test_end(self):
        self.assertEqual(
            dateparser.parse(self.raw_data["Date"].iloc[-1]).date(), self.ts.end
        )

    def test_duration(self):
        self.assertEqual(self.ts.end - self.ts.start, self.ts.duration)

    def test_values(self):
        self.assertTrue(self.raw_data["Close"].equals(self.ts.values))

    def test_dates(self):
        self.assertTrue(
            pd.to_datetime(self.raw_data["Date"]).dt.date.equals(self.ts.dates)
        )

    def test_time_values(self):
        data = self.raw_data[["Date", "Close"]].copy()
        data.Date = pd.to_datetime(data.Date).dt.date
        self.assertTrue((data.values == self.ts.time_values.values).all())

    def test_keep_recent_days(self):
        month_days = 30
        trimmed_series = self.ts.keep_recent_days(month_days)
        self.assertEqual(trimmed_series.duration, dt.timedelta(days=month_days - 1))
        self.assertEqual(trimmed_series.end, self.ts.end)

    def test_eq(self):
        self.assertEqual(self.ts, self.ts)
        self.assertNotEqual(self.ts, 0)

    def test_len(self):
        series = TimeSeries(
            "dummy",
            pd.DataFrame(data=[[dt.date(2020, 1, 1), 0], [dt.date(2020, 1, 2), 10]]),
        )
        self.assertEqual(len(series), 2)

    def test_json(self):
        self.assertEqual(self.ts, TimeSeries.from_json(self.ts.to_json()))

    def test_make_relative(self):
        first = TimeSeries(
            "1",
            pd.DataFrame(
                {
                    "date": [
                        dt.date(2020, 1, 7),
                        dt.date(2020, 1, 8),
                        dt.date(2020, 1, 9),
                    ],
                    "value": [1, 2, 3],
                }
            ),
        )
        second = TimeSeries(
            "2",
            pd.DataFrame(
                {
                    "date": [
                        dt.date(2020, 1, 8),
                        dt.date(2020, 1, 9),
                        dt.date(2020, 1, 10),
                    ],
                    "value": [3, 6, 9],
                }
            ),
        )
        third = TimeSeries(
            "3",
            pd.DataFrame(
                {
                    "date": [
                        dt.date(2020, 1, 8),
                        dt.date(2020, 1, 9),
                        dt.date(2020, 1, 10),
                    ],
                    "value": [1, 0, 1],
                }
            ),
        )
        relatives = make_relative([first, second, third])
        self.assertEqual(
            relatives[0],
            TimeSeries(
                "1 (rel)",
                pd.DataFrame(
                    {
                        "date": [
                            dt.date(2020, 1, 7),
                            dt.date(2020, 1, 8),
                            dt.date(2020, 1, 9),
                        ],
                        "value": [1.0, 2.0, 3.0],
                    }
                ),
            ),
        )
        self.assertEqual(
            relatives[1],
            TimeSeries(
                "2 (rel)",
                pd.DataFrame(
                    {
                        "date": [
                            dt.date(2020, 1, 8),
                            dt.date(2020, 1, 9),
                            dt.date(2020, 1, 10),
                        ],
                        "value": [2.0, 4.0, 6.0],
                    }
                ),
            ),
        )
        self.assertEqual(
            relatives[2],
            TimeSeries(
                "3 (rel)",
                pd.DataFrame(
                    {
                        "date": [
                            dt.date(2020, 1, 8),
                            dt.date(2020, 1, 9),
                            dt.date(2020, 1, 10),
                        ],
                        "value": [2.0, 0, 2.0],
                    }
                ),
            ),
        )


if __name__ == "__main__":
    unittest.main()
