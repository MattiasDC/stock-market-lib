import datetime
import json
from jsonschema import validate
import unittest

from stock_market.core import StockMarket, Ticker, SignalSequence, Sentiment
from stock_market.ext.signal import GoldenCrossSignalDetector
from stock_market.ext.updater import YahooFinanceStockUpdater

class TestDeathCrossSignalDetector(unittest.TestCase):

	def test_detect(self):
		spy = Ticker('SPY')
		start = datetime.date(2019, 1, 1)
		end = datetime.date(2020, 10, 1)
		sm = StockMarket(start, [spy])
		sm = YahooFinanceStockUpdater().update(end, sm)
		sequence = SignalSequence()
		detector = GoldenCrossSignalDetector(1, spy)
		sequence = detector.detect(start, end, sm, sequence)
		self.assertTrue(len(sequence.signals) >= 1)
		golden_cross = sequence.signals[-1]
		self.assertEqual(golden_cross.date, datetime.date(2020, 7, 6))
		self.assertEqual(golden_cross.ticker, spy)
		self.assertEqual(golden_cross.sentiment, Sentiment.BULLISH)

	def test_json(self):
		detector = GoldenCrossSignalDetector(1, Ticker('SPY'))
		json_str = detector.to_json()
		self.assertEqual(GoldenCrossSignalDetector.from_json(json_str), detector)
		validate(instance=json.loads(json_str), schema=GoldenCrossSignalDetector.json_schema())

if __name__ == '__main__':
    unittest.main()