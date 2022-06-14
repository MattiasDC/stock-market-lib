import datetime

import pandas as pd

from stock_market.core import TimeSeries
from stock_market.ext.indicator import ExponentialMovingAverage


def test_ema():
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
    ema = ExponentialMovingAverage(2)
    ema_series = ema(series)
    assert len(ema_series) == 3
    assert ema_series.values.iloc[0] == 0
    assert ema_series.values.iloc[1] > 5
    assert ema_series.values.iloc[2] > 5
    assert ema.lag_days() == 2
