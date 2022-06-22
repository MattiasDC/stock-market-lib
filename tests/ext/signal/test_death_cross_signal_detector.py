import datetime
import json

from jsonschema import validate

from stock_market.core import Sentiment, SignalSequence, StockMarket, Ticker
from stock_market.ext.signal import DeathCrossSignalDetector
from stock_market.ext.updater import YahooFinanceStockUpdater


async def test_detect():
    spy = Ticker("SPY")
    start = datetime.date(2019, 1, 1)
    end = datetime.date(2020, 6, 1)
    sm = StockMarket(start, [spy])
    sm = await YahooFinanceStockUpdater().update(end, sm)
    sequence = SignalSequence()
    detector = DeathCrossSignalDetector(1, spy)
    sequence = detector.detect(start, end, sm, sequence)
    assert len(sequence.signals) == 1
    death_cross = sequence.signals[0]
    assert death_cross.date == datetime.date(2020, 3, 31)
    assert death_cross.sentiment == Sentiment.BEARISH


def test_json():
    detector = DeathCrossSignalDetector(1, Ticker("SPY"))
    json_str = detector.to_json()
    DeathCrossSignalDetector.from_json(json_str) == detector
    validate(
        instance=json.loads(json_str), schema=DeathCrossSignalDetector.json_schema()
    )
