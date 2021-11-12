from .signal.signal_sequence import SignalSequence
from .stock_market import StockMarket
import datetime as dt
import json
import pandas as pd

class Engine:
	def __init__(self, stock_market, stock_market_updater, signal_detectors, updated_to = None):
		self.__stock_market = stock_market
		self.__stock_market_updater = stock_market_updater
		self.__signal_detectors = signal_detectors
		self.__signal_sequence = SignalSequence()
		self.__updated_to = updated_to
		if self.__updated_to is not None:
			self.update(self.__updated_to, True)

	def update(self, date, force=False):
		if self.__updated_to is None or date > self.__updated_to:
			self.__updated_to = date

		current_end = self.__stock_market.date
		if date <= current_end and not force:
			return
		self.__stock_market = self.__stock_market_updater.update(date, self.stock_market)
		for date in pd.date_range(current_end + dt.timedelta(days=1), date + dt.timedelta(days=1)):
			for detector in self.__signal_detectors:
				detector.detect(date.date(), self.__stock_market, self.signals)

	@property
	def stock_market_updater(self):
		return self.__stock_market_updater

	@property
	def signal_detectors(self):
		return self.__signal_detectors

	@property
	def stock_market(self):
		return self.__stock_market
		
	@property
	def signals(self):
		return self.__signal_sequence

	def to_json(self):
		return json.dumps({"stock_market" : self.stock_market.to_json(),
					       "signals" : self.signals.to_json(),
					       "stock_updater" : self.__stock_market_updater.to_json(),
					       "signal_detectors" : json.dumps([detector.to_json() for detector in self.__signal_detectors]),
					       "updated_to" : self.__updated_to.isoformat() if self.__updated_to is not None else "__NONE"})

	@staticmethod
	def from_json(json_str, stock_updater_factory, signal_detector_factory):
		json_obj = json.loads(json_str)
		updated_to_json = json_obj["updated_to"]
		engine = Engine(StockMarket.from_json(json_obj["stock_market"]),
				 	    stock_updater_factory.create(json_obj["stock_updater"]),
				        [signal_detector_factory.create(config) for config in json.loads(json_obj["signal_detectors"])],
				        dt.date.fromisoformat(updated_to_json) if updated_to_json != "__NONE" else None)
		engine.__signal_sequence == SignalSequence.from_json(json_obj["signals"])
		return engine
