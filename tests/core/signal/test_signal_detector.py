import datetime

import pytest

from stock_market.core import SignalDetector, StockMarket


@pytest.fixture
def name():
    return "TestSignal"


@pytest.fixture
def identifier():
    return 1


def test_name(identifier, name):
    assert SignalDetector(identifier, name).name == name


def test_identifier(identifier, name):
    assert SignalDetector(identifier, name).id == identifier


def test_is_valid(identifier, name):
    start = datetime.date(2000, 1, 1)
    sm = StockMarket(start, [])
    assert SignalDetector(identifier, name).is_valid(sm)
