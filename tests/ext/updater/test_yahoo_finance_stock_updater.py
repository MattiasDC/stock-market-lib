import datetime as dt
import json

from jsonschema import validate

from stock_market.core import StockMarket, Ticker
from stock_market.ext.updater import YahooFinanceStockUpdater


async def test_update():
    spy = Ticker("SPY")
    sm = StockMarket(dt.date(2000, 1, 3), [spy])
    assert sm.ohlc(spy) is None
    new_date = dt.date(2022, 1, 5)
    sm = await YahooFinanceStockUpdater().update(new_date, sm)
    ohlc = sm.ohlc(spy)
    assert ohlc is not None
    assert ohlc.end == new_date


def test_json():
    updater = YahooFinanceStockUpdater()
    json_str = updater.to_json()
    assert YahooFinanceStockUpdater.from_json(json_str) == updater
    validate(
        instance=json.loads(json_str), schema=YahooFinanceStockUpdater.json_schema()
    )
