import datetime

import pandas as pd
import pytest

from stock_market.core import OHLC, StockMarket, Ticker, TickerOHLC


@pytest.fixture
def spy():
    return Ticker("SPY")


@pytest.fixture
def ohlc():
    raw_data = pd.read_csv("tests/data/SPY.csv")
    return OHLC(
        raw_data.Date,
        raw_data.Open,
        raw_data.High,
        raw_data.Low,
        raw_data.Close,
    )


@pytest.fixture
def date():
    return datetime.date(2000, 2, 2)


@pytest.fixture
def sm(date, spy):
    return StockMarket(date, [spy])


def test_start_date(date, sm):
    assert sm.start_date == date


def test_tickers(spy, sm):
    assert sm.tickers == [spy]


def test_add_ticker(sm):
    qqq = Ticker("QQQ")
    new_sm = sm.add_ticker(qqq)
    assert qqq in new_sm.tickers
    assert qqq not in sm.tickers


def test_remove_ticker(sm, spy):
    assert spy in sm.tickers
    new_sm = sm.remove_ticker(spy)
    assert spy not in new_sm.tickers


def test_ohlc_and_update_ticker(sm, spy, ohlc):
    assert sm.ohlc(spy) is None
    new_sm = sm.update_ticker(TickerOHLC(spy, ohlc))
    assert new_sm.ohlc(spy).start == sm.start_date
    assert new_sm.ohlc(spy).end == ohlc.end
    assert sm != new_sm  # Original one should remain unchanged


def test_date(sm, date, spy, ohlc):
    assert sm.date == date
    sm = sm.update_ticker(TickerOHLC(spy, ohlc))
    assert sm.date == ohlc.end


def test_eq(sm):
    assert sm == sm
    assert sm != 0


def test_json(sm, date, spy, ohlc):
    sm = sm.update_ticker(TickerOHLC(spy, ohlc))
    assert sm == StockMarket.from_json(sm.to_json())
