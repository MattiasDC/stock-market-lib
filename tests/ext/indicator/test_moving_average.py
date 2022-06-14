import datetime

import pandas as pd

from stock_market.core import TimeSeries
from stock_market.ext.indicator import MovingAverage


def test_ma():
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
    assert len(ma_series) == 3
    assert ma_series.values.iloc[0] == 0
    assert ma_series.values.iloc[1] == 5
    assert ma_series.values.iloc[2] == 10
    assert ma.lag_days() == 2
