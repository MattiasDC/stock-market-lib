import datetime
import json

from stock_market_engine.core.signal.signal import Signal
from stock_market_engine.core.signal.signal_detector import SignalDetector

class FixedIntervalSignal(Signal):
	def __init__(self, date, intervalName):
		super().__init__(f"{intervalName} interval signal", date)
		self.__intervalName = intervalName

	def __repr__(self):
		return f"FixedIntervalSignal({self.__intervalName}, {repr(self.date)})"

class FixedIntervalSignalFactory:
	def __init__(self, intervalName):
		self.__intervalName = intervalName

	def create(self, date):
		return FixedIntervalSignal(date, self.__intervalName)


class MonthlySignalDetector(SignalDetector):
	def __init__(self):
		name = "monthly"
		super().__init__(name, FixedIntervalSignalFactory(name))

	def detect(self, date, stock_market, sequence):
		if date.day == 1:
			self.signal(date, sequence)

	def __eq__(self, other):
		return isinstance(other, MonthlySignalDetector)

	def to_json(self):
		return json.dumps({})

	@staticmethod
	def from_json(json_str):
		return MonthlySignalDetector()

class BiMonthlySignalDetector(SignalDetector):
	def __init__(self):
		name = "bimonthly"
		super().__init__(name, FixedIntervalSignalFactory(name))

	def detect(self, date, stock_market, sequence):
		if date.day == 1 or date.day == 15:
			self.signal(date, sequence)

	def __eq__(self, other):
		return isinstance(other, BiMonthlySignalDetector)

	def to_json(self):
		return json.dumps({})

	@staticmethod
	def from_json(json_str):
		return BiMonthlySignalDetector()