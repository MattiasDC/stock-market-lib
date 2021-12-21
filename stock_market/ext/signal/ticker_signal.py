import json

from stock_market.core import Signal

class TickerSignal(Signal):
	def __init__(self, identifier, name, sentiment, ticker, date):
		super().__init__(identifier, f"{name} ({ticker})", sentiment, date)
		self.__ticker = ticker

	@property
	def ticker(self):
		return self.__ticker

	def __eq__(self, other):
		if not isinstance(other, TickerSignal):
			return False
		if not super().__eq__(other):
			return False
		return self.ticker == other.ticker

	def to_json(self):
		return json.dumps({"signal" : super().to_json(),
						   "ticker" : self.ticker.to_json()})

	@staticmethod
	def from_json(json_str):
		json_obj = json.loads(json_str)
		signal = json.loads(json_obj["signal"])
		return TickerSignal(signal.id,
							signal.name,
							signal.sentiment,
					 		json.loads(json_obj["ticker"]),
					 		signal.date)

	@staticmethod
	def json_schema():
		return { "type": "object",
  				 "properties": {
    			 	"signal": Signal.json_schema(),
    			 	"ticker" : Ticker.json_schema()
    			 }
    		   }