
class Ticker:
	def __init__(self, symbol):
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