import json

class Ticker:
	def __init__(self, symbol: str):
		assert len(symbol) <= 10
		self.__symbol = symbol

	@property
	def symbol(self):
		return self.__symbol

	def __eq__(self, other):
		if not isinstance(other, Ticker):
			return False
		return self.__symbol == other.__symbol

	def __hash__(self):
		return hash(self.__symbol)

	def __repr__(self):
		return f"Ticker({self.symbol})"

	def to_json(self):
		return json.dumps({"symbol" : self.symbol})

	@staticmethod
	def from_json(json_str):
		return Ticker(**json.loads(json_str))