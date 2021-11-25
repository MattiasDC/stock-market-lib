import json

from stock_market.core import add_signal
from stock_market.core import Signal, SignalDetector, SignalSequence

class BiMonthlySignalDetector(SignalDetector):
	def __init__(self, identifier):
		super().__init__(identifier, BiMonthlySignalDetector.NAME())

	def detect(self, date, stock_market):
		sequence = SignalSequence()
		if date.day == 1 or date.day == 15:
			sequence = add_signal(sequence, Signal(self.id, self.name, date))
		return sequence

	def __eq__(self, other):
		return isinstance(other, BiMonthlySignalDetector)

	@staticmethod
	def NAME():
		return "bimonthly"

	def to_json(self):
		return json.dumps({"id" : self.id})

	@staticmethod
	def from_json(json_str):
		return BiMonthlySignalDetector(json.loads(json_str)["id"])

	@staticmethod
	def json_schema():
		return { "type": "object",
  				 "properties": {
    			 	"id": { "type": "integer" }
    			 }
    		   }