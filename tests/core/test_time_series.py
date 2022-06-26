import datetime as dt

import dateparser
import pandas as pd
import pytest

from stock_market.core import TimeSeries
from stock_market.core.time_series import make_relative


@pytest.fixture
def raw_data():
    return pd.read_csv("tests/data/SPY.csv")


@pytest.fixture
def ts(raw_data):
    return TimeSeries("Close", raw_data[["Date", "Close"]])


def test_name(ts):
    assert "Close" == ts.name


def test_start(ts, raw_data):
    assert dateparser.parse(raw_data["Date"].iloc[0]).date() == ts.start


def test_end(ts, raw_data):
    assert dateparser.parse(raw_data["Date"].iloc[-1]).date() == ts.end


def test_duration(ts):
    assert ts.end - ts.start == ts.duration


def test_values(ts, raw_data):
    assert raw_data["Close"].equals(ts.values)


def test_dates(ts, raw_data):
    assert pd.to_datetime(raw_data["Date"]).dt.date.equals(ts.dates)


def test_time_values(ts, raw_data):
    data = raw_data[["Date", "Close"]].copy()
    data.Date = pd.to_datetime(data.Date).dt.date
    assert (data.values == ts.time_values.values).all()


def test_keep_recent_days(ts):
    month_days = 30
    trimmed_series = ts.keep_recent_days(month_days)
    assert trimmed_series.duration == dt.timedelta(days=month_days - 1)
    assert trimmed_series.end == ts.end


def test_start_at(ts):
    same_series = ts.start_at(ts.start)
    assert same_series == ts
    trimmed_series = ts.start_at(ts.start + dt.timedelta(days=2))
    assert trimmed_series.start >= ts.start + dt.timedelta(days=2)
    single_value_series = ts.start_at(ts.end)
    assert len(single_value_series.values) == 1


def test_end_at(ts):
    same_series = ts.end_at(ts.end + dt.timedelta(days=1))
    assert same_series == ts
    trimmed_series = ts.end_at(ts.end - dt.timedelta(days=2))
    assert trimmed_series.end <= ts.end + dt.timedelta(days=1)
    single_value_series = ts.end_at(ts.start + dt.timedelta(days=1))
    assert len(single_value_series.values) == 1


def test_trim(ts):
    same_series = ts.trim(ts.start, ts.end + dt.timedelta(days=1))
    assert same_series == ts
    trimmed_series = ts.trim(
        ts.start + dt.timedelta(days=1), ts.end - dt.timedelta(days=2)
    )
    assert trimmed_series.end <= ts.end + dt.timedelta(days=1)
    assert trimmed_series.start >= ts.start + dt.timedelta(days=2)


def test_eq(ts):
    assert ts == ts
    assert ts != 0


def test_len():
    series = TimeSeries(
        "dummy",
        pd.DataFrame(data=[[dt.date(2020, 1, 1), 0], [dt.date(2020, 1, 2), 10]]),
    )
    assert len(series) == 2


def test_json(ts):
    assert ts == TimeSeries.from_json(ts.to_json())


def test_make_relative():
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
    assert relatives[0] == TimeSeries(
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
    )

    assert relatives[1] == TimeSeries(
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
    )

    assert relatives[2] == TimeSeries(
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
    )
