import datetime
import unittest

import pandas as pd

from stock_market.core import TimeSeries
from stock_market.ext.indicator import MovingAverage


class TestMovingAverage(unittest.TestCase):
    def test_ma(self):
        series = TimeSeries(
            "dummy",
            pd.DataFrame(
                data=[
                    [datetime.date(2020, 1, 1), 0],
                    [datetime.date(2020, 1, 2), 10],
                    [datetime.date(2020, 1, 3), 10],
                ]
            ),
        )
        ma = MovingAverage(2)
        ma_series = ma(series)
        self.assertEqual(len(ma_series), 3)
        self.assertEqual(ma_series.values.iloc[0], 0)
        self.assertEqual(ma_series.values.iloc[1], 5)
        self.assertEqual(ma_series.values.iloc[2], 10)
        self.assertEqual(ma.lag_days(), 2)


if __name__ == "__main__":
    unittest.main()
