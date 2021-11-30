import json

from stock_market.common.single_attribute_json_mixin import SingleAttributeJsonMixin

class Ticker(SingleAttributeJsonMixin):
	JSON_ATTRIBUTE_NAME = "symbol"
	JSON_ATTRIBUTE_TYPE = "string"

	def __init__(self, symbol: str):
		assert len(symbol) <= 10
		self.__symbol = symbol

	@property
	def symbol(self):
		return self.__symbol

	def __eq__(self, other):
		if not isinstance(other, Ticker):
			return False
		return self.symbol == other.symbol

	def __hash__(self):
		return hash(self.symbol)

	def __repr__(self):
		return f"Ticker({self.symbol})"