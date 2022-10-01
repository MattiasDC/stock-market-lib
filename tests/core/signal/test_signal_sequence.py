import datetime

import pytest

from stock_market.core import (
    Sentiment,
    Signal,
    SignalSequence,
    add_signal,
    merge_signals,
)


@pytest.fixture
def name():
    return "TestSignal"


@pytest.fixture
def date():
    return datetime.date(2022, 1, 3)


@pytest.fixture
def signal(date):
    return Signal(1, "1", Sentiment.NEUTRAL, date)


@pytest.fixture
def second_signal(date):
    return Signal(2, "2", Sentiment.NEUTRAL, date)


@pytest.fixture
def third_signal(date):
    return Signal(3, "3", Sentiment.NEUTRAL, date + datetime.timedelta(days=1))


def test_add_signals(signal, second_signal, third_signal):
    ss = SignalSequence()
    ss = add_signal(ss, signal)
    assert ss.signals == [signal]
    ss = add_signal(ss, second_signal)
    assert ss.signals == [signal, second_signal]
    ss = add_signal(ss, third_signal)
    assert ss.signals == [signal, second_signal, third_signal]


def test_merge_signals(date, signal, second_signal, third_signal):
    first = SignalSequence()
    first = add_signal(first, signal)
    first = add_signal(first, second_signal)
    first = add_signal(first, third_signal)

    signal4 = Signal(4, "4", Sentiment.NEUTRAL, date - datetime.timedelta(days=1))
    signal5 = Signal(5, "5", Sentiment.NEUTRAL, date + datetime.timedelta(days=1))
    signal6 = Signal(6, "6", Sentiment.NEUTRAL, date + datetime.timedelta(days=2))
    second = SignalSequence()
    second = add_signal(second, signal4)
    second = add_signal(second, signal5)
    second = add_signal(second, signal6)

    merged = merge_signals(first, second, SignalSequence())
    assert merged.signals == [
        signal4,
        signal,
        second_signal,
        third_signal,
        signal5,
        signal6,
    ]


def test_signals_since(date, signal, second_signal, third_signal):
    signals = [signal, second_signal, third_signal]
    ss = SignalSequence(signals)
    assert ss.signals_since(date - datetime.timedelta(days=1)) == ss
    assert ss.signals_since(date) == SignalSequence([third_signal])


def test_eq(signal, second_signal, third_signal):
    assert SignalSequence() == SignalSequence()
    signals = [signal, second_signal, third_signal]
    ss = SignalSequence(signals)
    assert ss == ss
    assert ss != SignalSequence()
    assert ss != 0


def test_json(signal, second_signal, third_signal):
    signals = [signal, second_signal, third_signal]
    ss = SignalSequence(signals)
    assert ss == SignalSequence.from_json(ss.to_json())
