from .proxy_ohlc_fetcher import ProxyOHLCFetcher
from .yahoo_ohlc_fetcher import YahooOHLCFetcher


def register_ohlc_fetcher_factories(factory):
    factory = factory.register(
        "yahoo",
        YahooOHLCFetcher.from_json,
        YahooOHLCFetcher.json_schema(),
    )
    return factory.register(
        "proxy",
        ProxyOHLCFetcher.from_json,
        ProxyOHLCFetcher.json_schema(),
    )
