import datetime
import json
from jsonschema import validate
import unittest

from stock_market.core import StockMarket
from stock_market.core import Ticker
from stock_market.core import SignalSequence
from stock_market.ext.signal import BiMonthlySignalDetector


class TestBiMonthlySignalDetector(unittest.TestCase):
    def test_detect(self):
        spy = Ticker("SPY")
        sm = StockMarket(datetime.date(2000, 1, 1), [spy])
        sequence = SignalSequence()
        detector = BiMonthlySignalDetector(1)
        sequence = detector.detect(
            datetime.date(2000, 1, 2), datetime.date(2000, 1, 2), sm, sequence
        )
        self.assertFalse(sequence.signals)
        sequence = detector.detect(
            datetime.date(2000, 1, 15), datetime.date(2000, 1, 15), sm, sequence
        )
        self.assertEqual(len(sequence.signals), 1)
        sequence = detector.detect(
            datetime.date(2000, 2, 1), datetime.date(2000, 2, 1), sm, sequence
        )
        self.assertEqual(len(sequence.signals), 2)

        sequence = detector.detect(
            datetime.date(2001, 1, 1), datetime.date(2001, 12, 31), sm, sequence
        )
        self.assertEqual(len(sequence.signals), 26)

    def test_json(self):
        detector = BiMonthlySignalDetector(1)
        json_str = detector.to_json()
        self.assertEqual(BiMonthlySignalDetector.from_json(json_str), detector)
        validate(
            instance=json.loads(json_str), schema=BiMonthlySignalDetector.json_schema()
        )


if __name__ == "__main__":
    unittest.main()
