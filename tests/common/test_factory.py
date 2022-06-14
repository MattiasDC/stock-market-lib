import json

from stock_market.common.factory import Factory
from stock_market.ext.signal import (
    BiMonthlySignalDetector,
    MonthlySignalDetector,
    register_signal_detector_factories,
)


def test_create():
    factory = Factory()
    register_signal_detector_factories(factory)
    assert factory.create(
        MonthlySignalDetector.NAME(), json.dumps(1)
    ) == MonthlySignalDetector(1)
    assert factory.create(
        BiMonthlySignalDetector.NAME(), json.dumps(1)
    ) == BiMonthlySignalDetector(1)


def test_register():
    factory = Factory()
    factory.register(
        "m", MonthlySignalDetector.from_json, MonthlySignalDetector.json_schema()
    )
    assert factory.create("m", json.dumps(1)) == MonthlySignalDetector(1)


def test_registered_names():
    factory = Factory()
    assert not ("m" in factory.get_registered_names())
    factory.register(
        "m", MonthlySignalDetector.from_json, MonthlySignalDetector.json_schema()
    )
    assert "m" in factory.get_registered_names()


def test_get_schema():
    factory = Factory()
    factory.register(
        "m", MonthlySignalDetector.from_json, MonthlySignalDetector.json_schema()
    )
    assert factory.get_schema("m") is not None
