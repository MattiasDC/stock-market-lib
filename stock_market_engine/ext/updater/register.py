from .yahoo_finance_stock_updater import YahooFinanceStockUpdater

def register_stock_updater_factories(factory):
	factory.register("yahoo", lambda _: YahooFinanceStockUpdater())