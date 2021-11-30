from .bi_monthly_signal_detector import BiMonthlySignalDetector
from .crossover_signal_detector import CrossoverSignalDetector
from .death_cross_signal_detector import DeathCrossSignalDetector
from .golden_cross_signal_detector import GoldenCrossSignalDetector
from .monthly_signal_detector import MonthlySignalDetector

def register_signal_detector_factories(factory):
	factory.register(BiMonthlySignalDetector.NAME(), BiMonthlySignalDetector.from_json, BiMonthlySignalDetector.json_schema())
	factory.register(CrossoverSignalDetector.NAME(), CrossoverSignalDetector.from_json, CrossoverSignalDetector.json_schema())
	factory.register(DeathCrossSignalDetector.NAME(), DeathCrossSignalDetector.from_json, DeathCrossSignalDetector.json_schema())
	factory.register(GoldenCrossSignalDetector.NAME(), GoldenCrossSignalDetector.from_json, GoldenCrossSignalDetector.json_schema())
	factory.register(MonthlySignalDetector.NAME(), MonthlySignalDetector.from_json, MonthlySignalDetector.json_schema())
	return factory