from stock_market.core import StockUpdater


def test_name():
    assert StockUpdater("Test").name == "Test"
