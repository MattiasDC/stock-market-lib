
class SignalDetector:
	def __init__(self, name, signal_factory):
		self.__name = name
		self.__signal_factory = signal_factory

	@property
	def name(self):
		return self.__name

	def to_json(self):
		return {"name" : self.name}
		
	def signal(self, date, sequence):
		sequence.add(self.__signal_factory.create(date))