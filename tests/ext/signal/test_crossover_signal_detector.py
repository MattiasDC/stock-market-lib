import datetime
from itertools import islice
import json
from jsonschema import validate
import unittest

from utils.algos import all_equal

from stock_market.common.factory import Factory
from stock_market.core import (
    StockMarket,
    Ticker,
    SignalSequence,
    merge_signals,
    Sentiment,
)
from stock_market.ext.indicator import (
    Identity,
    ExponentialMovingAverage,
    register_indicator_factories,
)
from stock_market.ext.signal import CrossoverSignalDetector
from stock_market.ext.updater import YahooFinanceStockUpdater


class TestCrossoverSignalDetector(unittest.TestCase):
    def alternates_two_values(self, sequence):
        self.assertTrue(all_equal(islice(iter(sequence), 0, None, 2)))
        self.assertTrue(all_equal(islice(iter(sequence), 1, None, 2)))

        if len(sequence) > 1:
            self.assertNotEqual(sequence[0], sequence[1])

    def alternates_bullish_bearish(self, signal_sequence):
        signals = signal_sequence.signals

        def get_sentiment(s):
            return s.sentiment

        self.alternates_two_values(list(map(get_sentiment, signals)))

    def validate_crossovers(self, crossover_signals, series, indicator_series):
        crossover_indices = series.dates.loc[
            series.dates.isin(map(lambda s: s.date, crossover_signals.signals))
        ].index
        crossover_indices_and_before = crossover_indices.union(crossover_indices - 1)
        differences = (
            series.values.iloc[crossover_indices_and_before]
            - indicator_series.values.iloc[crossover_indices_and_before]
        )
        diff_gt_0 = (differences > 0).tolist()
        self.alternates_two_values(diff_gt_0)
        self.assertEqual(
            diff_gt_0[0], crossover_signals.signals[0].sentiment == Sentiment.BEARISH
        )

    def test_is_valid(self):
        start = datetime.date(2000, 1, 1)
        spy = Ticker("SPY")
        sm = StockMarket(start, [spy])
        ema = ExponentialMovingAverage(20)
        bullish_spy_detector = CrossoverSignalDetector(
            1, "Bullish SPY Crossover EMA(20)", spy, Identity(), ema, Sentiment.BULLISH
        )
        bullish_qqq_detector = CrossoverSignalDetector(
            1,
            "Bullish QQQ Crossover EMA(20)",
            Ticker("QQQ"),
            Identity(),
            ema,
            Sentiment.BULLISH,
        )
        self.assertTrue(bullish_spy_detector.is_valid(sm))
        self.assertFalse(bullish_qqq_detector.is_valid(sm))

    def test_detect(self):
        spy = Ticker("SPY")
        start = datetime.date(2000, 1, 1)
        start_plus_10 = datetime.date(2010, 1, 1)
        end = datetime.date(2021, 1, 1)
        sm = StockMarket(start, [spy])
        ema = ExponentialMovingAverage(20)
        bullish_detector = CrossoverSignalDetector(
            1, "Bullish SPY Crossover EMA(20)", spy, Identity(), ema, Sentiment.BULLISH
        )
        bearish_detector = CrossoverSignalDetector(
            1, "Bearish SPY Crossover EMA(20)", spy, Identity(), ema, Sentiment.BEARISH
        )
        sm = YahooFinanceStockUpdater().update(end, sm)
        bullish_signals = bullish_detector.detect(
            start_plus_10, end, sm, SignalSequence()
        )
        bearish_signals = bearish_detector.detect(
            start_plus_10, end, sm, SignalSequence()
        )
        signals = merge_signals(bullish_signals, bearish_signals)
        self.alternates_bullish_bearish(signals)

        first_crossover_date = signals.signals[0].date
        self.assertTrue(first_crossover_date >= start_plus_10)
        self.assertTrue(signals.signals[-1].date <= end)

        close_values_spy = sm.ohlc(spy).close
        ema_spy = ema(close_values_spy)
        self.validate_crossovers(bullish_signals, close_values_spy, ema_spy)
        self.validate_crossovers(bearish_signals, close_values_spy, ema_spy)

    def test_json(self):
        spy = Ticker("SPY")
        ema = ExponentialMovingAverage(20)
        detector = CrossoverSignalDetector(
            1, "Bullish SPY Crossover EMA(20)", spy, Identity(), ema, Sentiment.BULLISH
        )

        json_str = detector.to_json()
        factory = register_indicator_factories(Factory())
        self.assertEqual(CrossoverSignalDetector.from_json(json_str, factory), detector)
        validate(
            instance=json.loads(json_str), schema=CrossoverSignalDetector.json_schema()
        )


if __name__ == "__main__":
    unittest.main()
