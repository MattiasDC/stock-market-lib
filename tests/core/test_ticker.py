from stock_market.core import Ticker


def test_symbol():
    assert Ticker("Test").symbol == "Test"


def test_eq():
    assert Ticker("T") == Ticker("T")
    assert Ticker("A") != Ticker("T")
    assert Ticker("A") != 0


def test_json():
    assert Ticker("T") == Ticker.from_json(Ticker("T").to_json())
