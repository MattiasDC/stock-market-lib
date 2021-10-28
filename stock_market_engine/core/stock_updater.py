
class StockUpdater:
	def __init__(self, name):
		self.__name = name

	@property
	def name(self):
		return self.__name

	def to_json(self):
		return {"name" : self.__name}
		