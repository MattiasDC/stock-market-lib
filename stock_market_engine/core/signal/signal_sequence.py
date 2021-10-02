from heapq import merge

class SignalSequence:
	def __init__(self, signals=[]):
		self.__signals = signals

	@property
	def signals(self):
		return self.__signals

	"""
	Returns all signals since the given date.
	The given date is not included.
	"""
	def signals_since(self, date):
		return [s for s in self.signals if s.date > date]

	def add(self, signal):
		assert(signal not in self.__signals)
		assert(not self.__signals or signal.date >= self.__signals[-1].date)
		self.__signals.append(signal)