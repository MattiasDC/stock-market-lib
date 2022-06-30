import datetime
import json

from jsonschema import validate

from stock_market.core import (
    Sentiment,
    SignalSequence,
    StockMarket,
    StockUpdater,
    Ticker,
)
from stock_market.ext.fetcher.yahoo_ohlc_fetcher import YahooOHLCFetcher
from stock_market.ext.signal import GoldenCrossSignalDetector


async def test_detect():
    spy = Ticker("SPY")
    start = datetime.date(2019, 1, 1)
    end = datetime.date(2020, 10, 1)
    sm = StockMarket(start, [spy])
    sm = await StockUpdater(YahooOHLCFetcher()).update(end, sm)
    sequence = SignalSequence()
    detector = GoldenCrossSignalDetector(1, spy)
    sequence = detector.detect(start, end, sm, sequence)
    assert len(sequence.signals) >= 1
    golden_cross = sequence.signals[-1]
    assert golden_cross.date == datetime.date(2020, 7, 6)
    assert golden_cross.sentiment == Sentiment.BULLISH


def test_json():
    detector = GoldenCrossSignalDetector(1, Ticker("SPY"))
    json_str = detector.to_json()
    assert GoldenCrossSignalDetector.from_json(json_str) == detector
    validate(
        instance=json.loads(json_str),
        schema=GoldenCrossSignalDetector.json_schema(),
    )
