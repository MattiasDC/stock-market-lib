import pandas as pd
import pytest

from stock_market.core import OHLC, Ticker, TickerOHLC


@pytest.fixture
def ticker():
    return Ticker("Test")


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


def test_ticker(ticker, ohlc):
    ticker_ohlc = TickerOHLC(ticker, ohlc)
    assert ticker_ohlc.ticker == ticker


def test_ohlc(ticker, ohlc):
    ticker_ohlc = TickerOHLC(ticker, ohlc)
    assert ticker_ohlc.ohlc == ohlc
