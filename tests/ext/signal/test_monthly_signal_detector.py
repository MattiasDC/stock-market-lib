import datetime
import json

from jsonschema import validate

from stock_market.core import SignalSequence, StockMarket, Ticker
from stock_market.ext.signal import MonthlySignalDetector


def test_detect():
    spy = Ticker("SPY")
    sm = StockMarket(datetime.date(2000, 1, 1), [spy])
    sequence = SignalSequence()
    detector = MonthlySignalDetector(1)
    sequence = detector.detect(
        datetime.date(2000, 1, 2), datetime.date(2000, 1, 2), sm, sequence
    )
    assert not sequence.signals
    sequence = detector.detect(
        datetime.date(2000, 2, 1), datetime.date(2000, 2, 1), sm, sequence
    )
    assert len(sequence.signals) == 1
    sequence = detector.detect(
        datetime.date(2001, 1, 1), datetime.date(2001, 12, 31), sm, sequence
    )
    assert len(sequence.signals) == 13
    for s in sequence.signals:
        assert s.date.day == 1


def test_json():
    detector = MonthlySignalDetector(1)
    json_str = detector.to_json()
    assert MonthlySignalDetector.from_json(json_str) == detector
    validate(instance=json.loads(json_str), schema=MonthlySignalDetector.json_schema())
