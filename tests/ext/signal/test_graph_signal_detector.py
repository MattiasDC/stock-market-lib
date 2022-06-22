import datetime as dt

import pytest

from stock_market.common.factory import Factory
from stock_market.core import Sentiment, SignalSequence, StockMarket, Ticker
from stock_market.ext.indicator import ExponentialMovingAverage, Identity
from stock_market.ext.signal import (
    CrossoverSignalDetector,
    EnterOrExit,
    GraphSignalDetector,
    GraphSignalDetectorBuilder,
    register_signal_detector_factories,
)
from stock_market.ext.updater import YahooFinanceStockUpdater


@pytest.fixture
def arkk():
    return Ticker("ARKK")


@pytest.fixture
def start():
    return dt.date(2019, 12, 15)


@pytest.fixture
def end():
    return dt.date(2020, 4, 1)


@pytest.fixture
async def sm(start, end, arkk):
    stock_market = StockMarket(start, [arkk])
    stock_market = await YahooFinanceStockUpdater().update(end, stock_market)
    return stock_market


@pytest.fixture
def builder(arkk):
    bearish_ema_50_crossover = CrossoverSignalDetector(
        1,
        "bear ema(50)",
        arkk,
        Identity(),
        ExponentialMovingAverage(50),
        Sentiment.BEARISH,
    )
    bearish_ema_5_7_crossover = CrossoverSignalDetector(
        2,
        "bear ema(5-7)",
        arkk,
        ExponentialMovingAverage(5),
        ExponentialMovingAverage(7),
        Sentiment.BEARISH,
    )
    bullish_ema_5_7_crossover = CrossoverSignalDetector(
        3,
        "bear ema(5-7)",
        arkk,
        ExponentialMovingAverage(5),
        ExponentialMovingAverage(7),
        Sentiment.BULLISH,
    )
    bullish_ema_50_crossover = CrossoverSignalDetector(
        4,
        "bull ema(50)",
        arkk,
        Identity(),
        ExponentialMovingAverage(50),
        Sentiment.BULLISH,
    )
    """
                 -----------
                 |         | 3
            1    v     2   |
    none  ----> bear50-->hedge<---
    | ^          |         |     |
    | |-----------         |     |
    | |    4               |     |
    | |                    | 4   | 1
    | --------bear5/7<------     |
    |     3     ^  |             |
    |           |  ---------------
    |     2     |
    -------------
    """
    builder = GraphSignalDetectorBuilder(0)
    builder = builder.set_name("puru hedge")
    builder = builder.add_detector(bearish_ema_50_crossover)
    builder = builder.add_detector(bearish_ema_5_7_crossover)
    builder = builder.add_detector(bullish_ema_5_7_crossover)
    builder = builder.add_detector(bullish_ema_50_crossover)
    builder = builder.add_state("none")
    builder = builder.add_state("bear50")
    builder = builder.add_state("bear5/7")
    builder = builder.add_state("hedge")
    builder = builder.set_initial_state("none")
    builder = builder.add_signal_description(
        "hedge", Sentiment.BEARISH, EnterOrExit.ENTER
    )
    builder = builder.add_signal_description(
        "hedge", Sentiment.BULLISH, EnterOrExit.EXIT
    )
    builder = builder.add_transition("none", "bear50", bearish_ema_50_crossover.id)
    builder = builder.add_transition("bear50", "hedge", bearish_ema_5_7_crossover.id)
    builder = builder.add_transition("bear50", "none", bullish_ema_50_crossover.id)
    builder = builder.add_transition("hedge", "bear50", bullish_ema_5_7_crossover.id)
    builder = builder.add_transition("hedge", "bear5/7", bullish_ema_50_crossover.id)
    builder = builder.add_transition("none", "bear5/7", bearish_ema_5_7_crossover.id)
    builder = builder.add_transition("bear5/7", "hedge", bearish_ema_50_crossover.id)
    builder = builder.add_transition("bear5/7", "none", bullish_ema_5_7_crossover.id)
    return builder


@pytest.fixture
def puru_hedge_detector(builder):
    return builder.build()


def test_detector_signals(start, end, sm, puru_hedge_detector, arkk):
    sequence = puru_hedge_detector.detect(start, end, sm, SignalSequence())
    signals = sequence.signals
    assert len(signals) == 4
    assert signals[0].date == dt.date(2020, 2, 25)  # corona crisis
    assert signals[0].sentiment == Sentiment.BEARISH
    assert signals[0].tickers == [arkk]
    assert signals[1].date == dt.date(2020, 3, 4)
    assert signals[1].sentiment == Sentiment.BULLISH
    assert signals[1].tickers == [arkk]
    assert signals[2].date == dt.date(2020, 3, 5)
    assert signals[2].sentiment == Sentiment.BEARISH
    assert signals[2].tickers == [arkk]
    assert signals[3].date == dt.date(2020, 3, 25)
    assert signals[3].sentiment == Sentiment.BULLISH
    assert signals[3].tickers == [arkk]


def test_detector_json(puru_hedge_detector):
    detector_factory = register_signal_detector_factories(Factory())
    json_detector = GraphSignalDetector.from_json(
        puru_hedge_detector.to_json(), detector_factory
    )
    assert puru_hedge_detector == json_detector


def test_detector_factory(puru_hedge_detector):
    detector_factory = register_signal_detector_factories(Factory())
    assert puru_hedge_detector == detector_factory.create(
        GraphSignalDetector.NAME(), puru_hedge_detector.to_json()
    )


def test_builder_json(puru_hedge_detector, builder):
    detector_factory = register_signal_detector_factories(Factory())
    assert (
        puru_hedge_detector
        == GraphSignalDetectorBuilder.from_json(
            builder.to_json(), detector_factory
        ).build()
    )
