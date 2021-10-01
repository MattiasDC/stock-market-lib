from heapq import merge
from utils.algos import is_sorted

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
		return [s if s.date > date for s in self.signals]

	def add(self, signal):
		assert(signal not in self.__signals)
		assert(self.__signals || signal.date >= self.__signals[-1].date)
		self.__signals.append(signal)

	@staticmethod
	def merge(sequences):
		assert(all(is_sorted(s) for s in sequences))
		return SignalSequence(list(merge(*sequences)))