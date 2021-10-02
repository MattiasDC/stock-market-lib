from .core.signal.signal_sequence import SignalSequence

class Engine:
	def __init__(self, stock_market, stock_market_updater, signal_detectors):
		self.__stock_market = stock_market
		self.__stock_market_updater = stock_market_updater
		self.__signal_detectors = signal_detectors
		self.__signal_sequence = SignalSequence()

	def update(self, date):
		self.__stock_market_updater.update(date, self.__stock_market)
		for detector in self.__signal_detector:
			detector.detect(date, self.__stock_market, self.__signal_sequence)

	@property
	def stock_market(self):
		self.__stock_market
		
	@property
	def signals(self):
		return self.__signal_sequence.signals