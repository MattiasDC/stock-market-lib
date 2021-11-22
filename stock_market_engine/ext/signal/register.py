from .bi_monthly_signal_detector import BiMonthlySignalDetector
from .monthly_signal_detector import MonthlySignalDetector

def register_signal_detector_factories(factory):
	factory.register(MonthlySignalDetector.NAME(), MonthlySignalDetector.from_json)
	factory.register(BiMonthlySignalDetector.NAME(), BiMonthlySignalDetector.from_json)
	return factory