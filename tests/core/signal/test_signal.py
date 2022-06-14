import datetime

import pytest

from stock_market.core import Sentiment, Signal, Ticker


@pytest.fixture
def name():
    return "TestSignal"


@pytest.fixture
def identifier():
    return 1


@pytest.fixture
def sentiment():
    return Sentiment.BULLISH


@pytest.fixture
def date():
    return datetime.datetime.now().date()


@pytest.fixture
def spy():
    return Ticker("SPY")


@pytest.fixture
def qqq():
    return Ticker("QQQ")


@pytest.fixture
def signal(identifier, name, sentiment, date, spy, qqq):
    return Signal(identifier, name, sentiment, date, [spy, qqq])


def test_name(name, signal):
    assert signal.name == name


def test_id(identifier, signal):
    assert signal.id == identifier


def test_sentiment(sentiment, signal):
    assert signal.sentiment == sentiment


def test_date(date, signal):
    assert signal.date == date


def test_ticker(spy, qqq, signal):
    assert signal.tickers == [spy, qqq]


def test_eq(signal):
    assert signal == signal
    assert signal != 0


def test_json(signal):
    assert signal == Signal.from_json(signal.to_json())
