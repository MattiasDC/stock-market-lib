from .yahoo_finance_stock_updater import YahooFinanceStockUpdater


def register_stock_updater_factories(factory):
    return factory.register(
        "yahoo",
        YahooFinanceStockUpdater.from_json,
        YahooFinanceStockUpdater.json_schema(),
    )
