import datetime
import json
import unittest

from stock_market.common.factory import Factory
from stock_market.ext.signal import BiMonthlySignalDetector
from stock_market.ext.signal import MonthlySignalDetector
from stock_market.ext.signal import register_signal_detector_factories

class TestFactory(unittest.TestCase):

	def test_create(self):
		factory = Factory()
		register_signal_detector_factories(factory)
		self.assertEqual(factory.create(MonthlySignalDetector.NAME(), json.dumps({"id" : 1})), MonthlySignalDetector(1))
		self.assertEqual(factory.create(BiMonthlySignalDetector.NAME(), json.dumps({"id" : 1})), BiMonthlySignalDetector(1))

	def test_register(self):
		factory = Factory()
		factory.register("m", MonthlySignalDetector.from_json, MonthlySignalDetector.json_schema())
		self.assertEqual(factory.create("m", json.dumps({"id" : 1})), MonthlySignalDetector(1))

	def test_registered_names(self):
		factory = Factory()
		self.assertFalse("m" in factory.get_registered_names())
		factory.register("m", MonthlySignalDetector.from_json, MonthlySignalDetector.json_schema())
		self.assertTrue("m" in factory.get_registered_names())

	def test_get_schema(self):
		factory = Factory()
		factory.register("m", MonthlySignalDetector.from_json, MonthlySignalDetector.json_schema())
		self.assertNotEqual(factory.get_schema("m"), None)


if __name__ == '__main__':
    unittest.main()