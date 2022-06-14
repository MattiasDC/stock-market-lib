import datetime

import pandas as pd

from stock_market.core import TimeSeries
from stock_market.ext.indicator import Identity


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
    identity = Identity()
    identity_series = identity(series)
    assert identity_series == series
    assert identity.lag_days() == 0
