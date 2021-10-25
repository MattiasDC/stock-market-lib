import json
from .signal import Signal

class SignalSequence:
	def __init__(self, signals=None):
		if signals is None:
			self.__signals = []
		else:
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

	def __str__(self):
		signals_string = ", ".join(map(str, self.signals))
		return f"SignalSequence({signals_string})"

	def __repr__(self):
		signals_string = ", ".join(map(repr, self.signals))
		return f"SignalSequence({signals_string})"

	def __eq__(self, other):
		if not isinstance(other, SignalSequence):
			return False
		return self.signals == other.signals

	def to_json(self):
		return json.dumps([s.to_json() for s in self.signals])

	@staticmethod
	def from_json(json_str):
		return SignalSequence([Signal.from_json(s) for s in json.loads(json_str)])