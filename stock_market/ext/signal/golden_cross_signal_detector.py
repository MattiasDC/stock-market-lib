import json
import pandas as pd

from stock_market.core import add_signal
from stock_market.core import Signal, Sentiment, Ticker
from stock_market.ext.signal import CrossoverSignalDetector
from stock_market.ext.indicator import MovingAverage

class GoldenCrossSignalDetector(CrossoverSignalDetector):
	def __init__(self, identifier, ticker):
		super().__init__(identifier,
						 GoldenCrossSignalDetector.NAME(),
						 ticker,
						 MovingAverage(50),
						 MovingAverage(200),
						 Sentiment.BULLISH)

	@staticmethod
	def NAME():
		return "Golden cross"

	def to_json(self):
		return json.dumps({"id" : self.id,
						   "ticker" : self.ticker.to_json()})

	@staticmethod
	def from_json(json_str):
		json_obj = json.loads(json_str)
		return GoldenCrossSignalDetector(json_obj["id"], Ticker.from_json(json_obj["ticker"]))

	@staticmethod
	def json_schema():
		return { "type": "object",
  				 "properties": {
    			 	"id": { "type": "integer" },
    			 	"ticker" : { "type": "string" }
    			 }
    		   }