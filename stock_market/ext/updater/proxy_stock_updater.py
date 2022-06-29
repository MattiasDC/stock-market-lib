import aiohttp
from utils.logging import get_logger

from stock_market.common.json_mixins import SingleAttributeJsonMixin
from stock_market.core import OHLC, StockUpdater, Ticker, TickerOHLC

logger = get_logger(__name__)


class ProxyStockUpdater(StockUpdater, SingleAttributeJsonMixin):
    JSON_ATTRIBUTE_NAME = "api_url"
    JSON_ATTRIBUTE_TYPE = "string"

    def __init__(self, api_url):
        super().__init__("proxy")
        self.api_url = api_url

    async def update(self, date, stock_market):
        tickers = stock_market.tickers
        starts, ends = zip(
            *(
                self._get_period(stock_market, stock_market.ohlc(ticker), date)
                for ticker in tickers
            )
        )
        start_date, end_date = min(starts), max(ends)

        async with aiohttp.ClientSession() as client:
            response = await client.post(
                self.api_url,
                params={
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                },
                json={"tickers": [t.to_json() for t in tickers]},
            )
        ohlc_data = await response.json()
        for ticker, ohlc in ohlc_data.items():
            stock_market = stock_market.update_ticker(
                TickerOHLC(Ticker.from_json(ticker), OHLC.from_json(ohlc))
            )
        return stock_market

    def __eq__(self, other):
        if not isinstance(other, ProxyStockUpdater):
            return False
        return self.api_url == other.api_url
