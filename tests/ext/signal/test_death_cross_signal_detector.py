import datetime
import json
from jsonschema import validate
import unittest

from stock_market.core import StockMarket, Ticker, SignalSequence, Sentiment
from stock_market.ext.signal import DeathCrossSignalDetector
from stock_market.ext.updater import YahooFinanceStockUpdater

class TestDeathCrossSignalDetector(unittest.TestCase):

	def test_detect(self):
		spy = Ticker('SPY')
		start = datetime.date(2019, 1, 1)
		end = datetime.date(2020, 6, 1)
		sm = StockMarket(start, [spy])
		sm = YahooFinanceStockUpdater().update(end, sm)
		sequence = SignalSequence()
		detector = DeathCrossSignalDetector(1, spy)
		sequence = detector.detect(start, end, sm, sequence)
		self.assertEqual(len(sequence.signals), 1)
		death_cross = sequence.signals[0]
		self.assertEqual(death_cross.date, datetime.date(2020, 3, 31))
		self.assertEqual(death_cross.ticker, spy)
		self.assertEqual(death_cross.sentiment, Sentiment.BEARISH)

	def test_json(self):
		detector = DeathCrossSignalDetector(1, Ticker('SPY'))
		json_str = detector.to_json()
		self.assertEqual(DeathCrossSignalDetector.from_json(json_str), detector)
		validate(instance=json.loads(json_str), schema=DeathCrossSignalDetector.json_schema())

if __name__ == '__main__':
    unittest.main()