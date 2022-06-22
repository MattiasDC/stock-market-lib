import datetime
import json

from jsonschema import validate

from stock_market.core import Sentiment, SignalSequence, StockMarket, Ticker
from stock_market.ext.signal import GoldenCrossSignalDetector
from stock_market.ext.updater import YahooFinanceStockUpdater


async def test_detect():
    spy = Ticker("SPY")
    start = datetime.date(2019, 1, 1)
    end = datetime.date(2020, 10, 1)
    sm = StockMarket(start, [spy])
    sm = await YahooFinanceStockUpdater().update(end, sm)
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
