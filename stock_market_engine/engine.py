
class Engine:
	def __init__(self, stock_market, signal_detectors):
		self.__stock_market = stock_market
		self.__stock_market_updater = stock_market_updater
		self.__signal_detectors = signal_detectors
		self.__signal_sequences = [SignalSequence() for _ in range(len(signal_detectors))]

	def update(self, date):
		self.__stock_market_updater.update(date, stock_market)
		for i, detector in enumerate(self.__signal_detector):
			detector.detect(date, stock_market, self.__signal_sequences[i])