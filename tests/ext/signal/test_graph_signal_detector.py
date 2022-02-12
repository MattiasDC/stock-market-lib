import datetime as dt
import unittest

from stock_market.core import Sentiment, SignalSequence, StockMarket, Ticker
from stock_market.ext.indicator import ExponentialMovingAverage, Identity
from stock_market.ext.signal import (
    CrossoverSignalDetector,
    EnterOrExit,
    GraphSignalDetectorBuilder,
)
from stock_market.ext.updater import YahooFinanceStockUpdater


class TestGraphSignalDetector(unittest.TestCase):
    def test_detect(self):
        arkk = Ticker("ARKK")
        start = dt.date(2020, 1, 1)
        end = dt.date(2020, 4, 1)
        sm = StockMarket(start, [arkk])
        sm = YahooFinanceStockUpdater().update(end, sm)

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
        puru_hedge_detector_builder = GraphSignalDetectorBuilder(
            0,
            "puru hedge",
            arkk,
            [
                bearish_ema_50_crossover,
                bearish_ema_5_7_crossover,
                bullish_ema_5_7_crossover,
                bullish_ema_50_crossover,
            ],
            ["none", "bear50", "bear5/7", "hedge"],
            "none",
            [
                ("hedge", Sentiment.BEARISH, EnterOrExit.ENTER),
                ("hedge", Sentiment.BULLISH, EnterOrExit.EXIT),
            ],
            [
                {
                    "source": "none",
                    "dest": "bear50",
                    "trigger": bearish_ema_50_crossover.id,
                },
                {
                    "source": "bear50",
                    "dest": "hedge",
                    "trigger": bearish_ema_5_7_crossover.id,
                },
                {
                    "source": "bear50",
                    "dest": "none",
                    "trigger": bullish_ema_50_crossover.id,
                },
                {
                    "source": "hedge",
                    "dest": "bear50",
                    "trigger": bullish_ema_5_7_crossover.id,
                },
                {
                    "source": "hedge",
                    "dest": "bear5/7",
                    "trigger": bullish_ema_50_crossover.id,
                },
                {
                    "source": "none",
                    "dest": "bear5/7",
                    "trigger": bearish_ema_5_7_crossover.id,
                },
                {
                    "source": "bear5/7",
                    "dest": "hedge",
                    "trigger": bearish_ema_50_crossover.id,
                },
                {
                    "source": "bear5/7",
                    "dest": "none",
                    "trigger": bullish_ema_5_7_crossover.id,
                },
            ],
        )
        puru_hedge_detector = puru_hedge_detector_builder.build()

        sequence = puru_hedge_detector.detect(start, end, sm, SignalSequence())
        signals = sequence.signals
        self.assertEqual(len(signals), 2)

        self.assertEqual(signals[0].date, dt.date(2020, 2, 25))  # corona crisis
        self.assertEqual(signals[0].sentiment, Sentiment.BEARISH)

        self.assertEqual(signals[1].date, dt.date(2020, 3, 25))
        self.assertEqual(signals[1].sentiment, Sentiment.BULLISH)


if __name__ == "__main__":
    unittest.main()
