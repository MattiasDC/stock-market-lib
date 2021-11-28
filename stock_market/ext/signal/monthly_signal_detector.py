import json
import pandas as pd

from stock_market.core import add_signal, Signal, SignalDetector, Sentiment

class MonthlySignalDetector(SignalDetector):
	def __init__(self, identifier):
		super().__init__(identifier, MonthlySignalDetector.NAME())

	def detect(self, from_date, to_date, stock_market, sequence):
		for date in map(lambda d: d.date(), pd.date_range(from_date, to_date)):
			if date.day == 1:
				sequence = add_signal(sequence, Signal(self.id, self.name, Sentiment.NEUTRAL, date))
		return sequence

	def __eq__(self, other):
		return isinstance(other, MonthlySignalDetector)

	@staticmethod
	def NAME():
		return "Monthly"

	def to_json(self):
		return json.dumps({"id" : self.id})

	@staticmethod
	def from_json(json_str):
		return MonthlySignalDetector(json.loads(json_str)["id"])

	@staticmethod
	def json_schema():
		return { "type": "object",
  				 "properties": {
    			 	"id": { "type": "integer" }
    			 }
    		   }