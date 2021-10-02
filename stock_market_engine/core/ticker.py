
class Ticker:
	def __init__(self, symbol):
		self.__symbol = symbol

	@property
	def symbol(self):
		return self.__symbol