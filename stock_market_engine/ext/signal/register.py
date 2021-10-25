from .fixed_interval_signal import MonthlySignalDetector, BiMonthlySignalDetector

def register_signal_detector_factories(factory):
	factory.register("monthly", lambda _: MonthlySignalDetector())
	factory.register("bimonthly", lambda _: BiMonthlySignalDetector())