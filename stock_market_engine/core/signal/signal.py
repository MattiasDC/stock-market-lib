
class Signal:
	def __init__(self, name, date):
		self.__name = name
		self.__date = date

	@property
	def name(self):
		return self.__name

	@property
	def date(self):
		return self.__date

	def __repr__(self):
		return f"Signal({self.name}, {self.date})"

	def __str__(self):
		return self.__repr__()