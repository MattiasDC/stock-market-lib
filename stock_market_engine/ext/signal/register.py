from .fixed_interval_signal import MonthlySignalDetector, BiMonthlySignalDetector

def register_signal_detector_factories(factory):
	factory.register(MonthlySignalDetector().name, lambda _: MonthlySignalDetector())
	factory.register(BiMonthlySignalDetector().name, lambda _: BiMonthlySignalDetector())