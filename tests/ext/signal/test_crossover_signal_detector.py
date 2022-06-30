import datetime
import json
from itertools import islice

from jsonschema import validate
from utils.algos import all_equal

from stock_market.common.factory import Factory
from stock_market.core import (
    Sentiment,
    SignalSequence,
    StockMarket,
    StockUpdater,
    Ticker,
    merge_signals,
)
from stock_market.ext.fetcher.yahoo_ohlc_fetcher import YahooOHLCFetcher
from stock_market.ext.indicator import (
    ExponentialMovingAverage,
    Identity,
    register_indicator_factories,
)
from stock_market.ext.signal import CrossoverSignalDetector


def alternates_two_values(sequence):
    assert all_equal(islice(iter(sequence), 0, None, 2))
    assert all_equal(islice(iter(sequence), 1, None, 2))
    if len(sequence) > 1:
        assert sequence[0] != sequence[1]


def alternates_bullish_bearish(signal_sequence):
    signals = signal_sequence.signals

    def get_sentiment(s):
        return s.sentiment

    alternates_two_values(list(map(get_sentiment, signals)))


def validate_crossovers(crossover_signals, series, indicator_series):
    crossover_indices = series.dates.loc[
        series.dates.isin(map(lambda s: s.date, crossover_signals.signals))
    ].index
    crossover_indices_and_before = crossover_indices.union(crossover_indices - 1)
    differences = (
        series.values.iloc[crossover_indices_and_before]
        - indicator_series.values.iloc[crossover_indices_and_before]
    )
    diff_gt_0 = (differences > 0).tolist()
    alternates_two_values(diff_gt_0)
    assert diff_gt_0[0] == (crossover_signals.signals[0].sentiment == Sentiment.BEARISH)


def test_is_valid():
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
    assert bullish_spy_detector.is_valid(sm)
    assert not bullish_qqq_detector.is_valid(sm)


async def test_detect():
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
    sm = await StockUpdater(YahooOHLCFetcher()).update(end, sm)
    bullish_signals = bullish_detector.detect(start_plus_10, end, sm, SignalSequence())
    bearish_signals = bearish_detector.detect(start_plus_10, end, sm, SignalSequence())
    signals = merge_signals(bullish_signals, bearish_signals)
    alternates_bullish_bearish(signals)
    first_crossover_date = signals.signals[0].date
    assert first_crossover_date >= start_plus_10
    assert signals.signals[-1].date <= end
    close_values_spy = sm.ohlc(spy).close
    ema_spy = ema(close_values_spy)
    validate_crossovers(bullish_signals, close_values_spy, ema_spy)
    validate_crossovers(bearish_signals, close_values_spy, ema_spy)


def test_json():
    spy = Ticker("SPY")
    ema = ExponentialMovingAverage(20)
    detector = CrossoverSignalDetector(
        1, "Bullish SPY Crossover EMA(20)", spy, Identity(), ema, Sentiment.BULLISH
    )
    json_str = detector.to_json()
    factory = register_indicator_factories(Factory())
    assert CrossoverSignalDetector.from_json(json_str, factory) == detector
    validate(
        instance=json.loads(json_str), schema=CrossoverSignalDetector.json_schema()
    )
