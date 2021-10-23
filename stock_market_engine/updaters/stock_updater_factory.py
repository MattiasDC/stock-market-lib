from .yahoo_finance_stock_updater import YahooFinanceStockUpdater

class StockUpdaterFactory:
	def create(self, config):
		if config == "yahoo":
			return YahooFinanceStockUpdater()
			
		assert False, "Unsupported stock updater"