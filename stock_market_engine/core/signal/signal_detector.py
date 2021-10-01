
class SignalDetector:
	def __init__(self, signal_factory):
		self.__signal_factory = signal_factory

	def signal(self, date, sequence):
		sequence.add(self.__signal_factory.create(date))