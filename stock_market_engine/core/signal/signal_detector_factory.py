from stock_market_engine.ext.signal.fixed_interval_signal import MonthlySignalDetector, BiMonthlySignalDetector

class SignalDetectorFactory:
	def __init__(self):
		self.creator_map = {}

	def register(self, name, creator):
		assert name not in self.creator_map
		self.creator_map[name] = creator

	def create(self, config):
		assert config['name'] in self.creator_map
		return self.creator_map[config.pop('name')](config)