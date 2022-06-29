from .proxy_stock_updater import ProxyStockUpdater
from .yahoo_finance_stock_updater import YahooFinanceStockUpdater


def register_stock_updater_factories(factory):
    factory = factory.register(
        "yahoo",
        YahooFinanceStockUpdater.from_json,
        YahooFinanceStockUpdater.json_schema(),
    )
    return factory.register(
        "proxy",
        ProxyStockUpdater.from_json,
        ProxyStockUpdater.json_schema(),
    )
