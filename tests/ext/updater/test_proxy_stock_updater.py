import datetime as dt
import json
from functools import partial

import pandas as pd
import pytest
from aioresponses import CallbackResult
from jsonschema import validate

from stock_market.core import OHLC, StockMarket, Ticker
from stock_market.ext.updater import ProxyStockUpdater


@pytest.fixture
def start_date():
    return dt.date(2021, 1, 4)


@pytest.fixture
def end_date():
    return dt.date(2021, 1, 8)


@pytest.fixture
def ohlc(start_date, end_date):
    raw_data = pd.read_csv("tests/data/SPY.csv")

    return OHLC(
        raw_data.Date,
        raw_data.Open,
        raw_data.High,
        raw_data.Low,
        raw_data.Close,
    ).trim(start_date, end_date)


@pytest.fixture
def mock_url():
    return "https://mock:8080/ohlc"


@pytest.fixture
def proxy_updater(mock_url):
    return ProxyStockUpdater(mock_url)


def create_response(
    ohlc, assert_ticker, assert_start_date, assert_end_date, urk, **kwargs
):
    json_data = kwargs["json"]
    assert dt.date.fromisoformat(json_data["start_date"]) == assert_start_date
    assert dt.date.fromisoformat(json_data["end_date"]) == assert_end_date
    assert [assert_ticker] == [Ticker.from_json(t) for t in json_data["tickers"]]
    return CallbackResult(body=json.dumps({assert_ticker.to_json(): ohlc.to_json()}))


async def test_update(
    ohlc, mock_url, proxy_updater, start_date, end_date, aioresponses
):
    spy = Ticker("SPY")

    aioresponses.post(
        mock_url, callback=partial(create_response, ohlc, spy, start_date, end_date)
    )
    sm = StockMarket(start_date, [spy])
    assert sm.ohlc(spy) is None

    sm = await proxy_updater.update(end_date, sm)
    ohlc = sm.ohlc(spy)
    assert ohlc is not None
    assert ohlc.end == end_date - dt.timedelta(days=1)


def test_json(proxy_updater):
    json_str = proxy_updater.to_json()
    assert ProxyStockUpdater.from_json(json_str) == proxy_updater
    validate(instance=json.loads(json_str), schema=ProxyStockUpdater.json_schema())
