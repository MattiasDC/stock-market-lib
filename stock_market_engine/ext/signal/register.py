from .fixed_interval_signal import MonthlySignalDetector, BiMonthlySignalDetector

def register_signal_detector_factories(factory):
	factory.register(MonthlySignalDetector(None).name, MonthlySignalDetector.from_json)
	factory.register(BiMonthlySignalDetector(None).name, BiMonthlySignalDetector.from_json)
	return factory