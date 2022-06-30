import datetime as dt
import json

from jsonschema import validate

from stock_market.core import StockMarket, StockUpdater, Ticker
from stock_market.ext.fetcher import YahooOHLCFetcher


async def test_update():
    spy = Ticker("SPY")
    sm = StockMarket(dt.date(2000, 1, 3), [spy])
    assert sm.ohlc(spy) is None
    new_date = dt.date(2022, 1, 5)
    sm = await StockUpdater(YahooOHLCFetcher()).update(new_date, sm)
    ohlc = sm.ohlc(spy)
    assert ohlc is not None
    assert ohlc.end == new_date - dt.timedelta(days=1)


def test_json():
    fetcher = YahooOHLCFetcher()
    json_str = fetcher.to_json()
    assert YahooOHLCFetcher.from_json(json_str) == fetcher
    validate(instance=json.loads(json_str), schema=YahooOHLCFetcher.json_schema())
