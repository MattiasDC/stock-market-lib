import datetime as dt
import json
from functools import partial

import pandas as pd
import pytest
from aioresponses import CallbackResult
from jsonschema import validate

from stock_market.core import OHLC, StockMarket, StockUpdater, Ticker
from stock_market.ext.fetcher import ProxyOHLCFetcher


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
def proxy_ohlc_fetcher(mock_url):
    return ProxyOHLCFetcher(mock_url)


@pytest.fixture
def proxy_updater(proxy_ohlc_fetcher):
    return StockUpdater(proxy_ohlc_fetcher)


def create_response(
    ohlc, assert_ticker, assert_start_date, assert_end_date, urk, **kwargs
):
    json_data = kwargs["json"]["requests"][0]
    assert dt.date.fromisoformat(json_data["start_date"]) == assert_start_date
    assert dt.date.fromisoformat(json_data["end_date"]) == assert_end_date
    assert assert_ticker == Ticker(json_data["ticker"]["symbol"])
    return CallbackResult(body=json.dumps([(assert_ticker.to_json(), ohlc.to_json())]))


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


def test_json(proxy_ohlc_fetcher):
    json_str = proxy_ohlc_fetcher.to_json()
    assert ProxyOHLCFetcher.from_json(json_str) == proxy_ohlc_fetcher
    validate(instance=json.loads(json_str), schema=ProxyOHLCFetcher.json_schema())
