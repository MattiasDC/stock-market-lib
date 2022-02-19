import datetime as dt
import unittest

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


class TestGraphSignalDetector(unittest.TestCase):
    def setUp(self):

        self.arkk = Ticker("ARKK")
        self.start = dt.date(2020, 1, 1)
        self.end = dt.date(2020, 4, 1)
        sm = StockMarket(self.start, [self.arkk])
        self.sm = YahooFinanceStockUpdater().update(self.end, sm)

        bearish_ema_50_crossover = CrossoverSignalDetector(
            1,
            "bear ema(50)",
            self.arkk,
            Identity(),
            ExponentialMovingAverage(50),
            Sentiment.BEARISH,
        )
        bearish_ema_5_7_crossover = CrossoverSignalDetector(
            2,
            "bear ema(5-7)",
            self.arkk,
            ExponentialMovingAverage(5),
            ExponentialMovingAverage(7),
            Sentiment.BEARISH,
        )
        bullish_ema_5_7_crossover = CrossoverSignalDetector(
            3,
            "bear ema(5-7)",
            self.arkk,
            ExponentialMovingAverage(5),
            ExponentialMovingAverage(7),
            Sentiment.BULLISH,
        )
        bullish_ema_50_crossover = CrossoverSignalDetector(
            4,
            "bull ema(50)",
            self.arkk,
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
        builder = builder.add_transition(
            "bear50", "hedge", bearish_ema_5_7_crossover.id
        )
        builder = builder.add_transition("bear50", "none", bullish_ema_50_crossover.id)
        builder = builder.add_transition(
            "hedge", "bear50", bullish_ema_5_7_crossover.id
        )
        builder = builder.add_transition(
            "hedge", "bear5/7", bullish_ema_50_crossover.id
        )
        builder = builder.add_transition(
            "none", "bear5/7", bearish_ema_5_7_crossover.id
        )
        builder = builder.add_transition(
            "bear5/7", "hedge", bearish_ema_50_crossover.id
        )
        builder = builder.add_transition(
            "bear5/7", "none", bullish_ema_5_7_crossover.id
        )
        self.builder = builder
        self.puru_hedge_detector = builder.build()

    def test_detector_signals(self):

        sequence = self.puru_hedge_detector.detect(
            self.start, self.end, self.sm, SignalSequence()
        )
        signals = sequence.signals
        self.assertEqual(len(signals), 2)

        self.assertEqual(signals[0].date, dt.date(2020, 2, 25))  # corona crisis
        self.assertEqual(signals[0].sentiment, Sentiment.BEARISH)
        self.assertEqual(signals[0].tickers, [self.arkk])

        self.assertEqual(signals[1].date, dt.date(2020, 3, 25))
        self.assertEqual(signals[1].sentiment, Sentiment.BULLISH)
        self.assertEqual(signals[1].tickers, [self.arkk])

    def test_detector_json(self):
        detector_factory = register_signal_detector_factories(Factory())
        json_detector = GraphSignalDetector.from_json(
            self.puru_hedge_detector.to_json(), detector_factory
        )
        self.assertEqual(self.puru_hedge_detector, json_detector)

    def test_detector_factory(self):
        detector_factory = register_signal_detector_factories(Factory())
        self.assertEqual(
            self.puru_hedge_detector,
            detector_factory.create(
                GraphSignalDetector.NAME(), self.puru_hedge_detector.to_json()
            ),
        )

    def test_builder_json(self):
        detector_factory = register_signal_detector_factories(Factory())
        self.assertEqual(
            self.puru_hedge_detector,
            GraphSignalDetectorBuilder.from_json(
                self.builder.to_json(), detector_factory
            ).build(),
        )


if __name__ == "__main__":
    unittest.main()
