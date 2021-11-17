from .fixed_interval_signal import MonthlySignalDetector, BiMonthlySignalDetector

def register_signal_detector_factories(factory):
	factory.register(MonthlySignalDetector().name, MonthlySignalDetector.from_json)
	factory.register(BiMonthlySignalDetector().name, BiMonthlySignalDetector.from_json)
	return factory