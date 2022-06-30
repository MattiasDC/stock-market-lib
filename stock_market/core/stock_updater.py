from .ohlc import merge_ohlcs
from .ticker_ohlc import TickerOHLC


class StockUpdater:
    def __init__(self, ohlc_fetcher):
        self.__ohlc_fetcher = ohlc_fetcher

    def __update_ticker(self, stock_market, ticker, ohlc):
        if ohlc is None:
            return stock_market
        old_ohlc = stock_market.ohlc(ticker)
        return stock_market.update_ticker(
            TickerOHLC(ticker, merge_ohlcs(old_ohlc, ohlc))
        )

    def _get_period(self, stock_market, ticker, date):
        ohlc = stock_market.ohlc(ticker)
        if ohlc is None:
            return stock_market.start_date, date
        return ohlc.end, date

    async def update(self, date, stock_market):
        requests = [
            self._get_period(stock_market, t, date) + (t,) for t in stock_market.tickers
        ]
        async for ticker, ohlc in self.__ohlc_fetcher.fetch_ohlc(requests):
            stock_market = self.__update_ticker(stock_market, ticker, ohlc)
        return stock_market
