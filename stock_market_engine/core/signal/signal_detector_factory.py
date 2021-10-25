from stock_market_engine.ext.signal.fixed_interval_signal import MonthlySignalDetector, BiMonthlySignalDetector

class SignalDetectorFactory:
	def create(self, config):
		if config["name"] == "monthly":
			return MonthlySignalDetector()
		elif config["name"] == "bimonthly":
			return BiMonthlySignalDetector()
		assert False, "Unsupported signal detector"
