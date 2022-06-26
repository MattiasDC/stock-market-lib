import datetime as dt

import dateparser
import pandas as pd
import pytest

from stock_market.core import OHLC


@pytest.fixture
def raw_data():
    return pd.read_csv("tests/data/SPY.csv")


@pytest.fixture
def ohlc(raw_data):
    return OHLC(
        raw_data.Date,
        raw_data.Open,
        raw_data.High,
        raw_data.Low,
        raw_data.Close,
    )


def test_start(raw_data, ohlc):
    assert dateparser.parse(raw_data["Date"].iloc[0]).date() == ohlc.start


def test_end(raw_data, ohlc):
    assert dateparser.parse(raw_data["Date"].iloc[-1]).date() == ohlc.end


def test_dates(raw_data, ohlc):
    assert pd.to_datetime(raw_data["Date"]).dt.date.equals(ohlc.dates)


def test_open(raw_data, ohlc):
    assert (raw_data["Open"].values == ohlc.open.values).all()


def test_high(raw_data, ohlc):
    assert (raw_data["High"].values == ohlc.high.values).all()


def test_loq(raw_data, ohlc):
    assert (raw_data["Low"].values == ohlc.low.values).all()


def test_close(raw_data, ohlc):
    assert (raw_data["Close"].values == ohlc.close.values).all()


def test_keep_recent_days(ohlc):
    recent = ohlc.keep_recent_days(10)
    assert recent.end - recent.start == dt.timedelta(days=9)
    assert recent.end == ohlc.end
    assert recent.start == ohlc.end - dt.timedelta(days=9)


def test_trim(ohlc):
    same_ohlc = ohlc.trim(ohlc.start, ohlc.end + dt.timedelta(days=1))
    assert same_ohlc == ohlc
    trimmed_ohlc = ohlc.trim(
        ohlc.start + dt.timedelta(days=1), ohlc.end - dt.timedelta(days=2)
    )
    assert trimmed_ohlc.end <= ohlc.end + dt.timedelta(days=1)
    assert trimmed_ohlc.start >= ohlc.start + dt.timedelta(days=2)


def test_eq(ohlc):
    assert ohlc == ohlc
    assert ohlc != 0


def test_json(ohlc):
    assert ohlc == OHLC.from_json(ohlc.to_json())
