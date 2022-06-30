import aiohttp
from utils.logging import get_logger

from stock_market.common.json_mixins import SingleAttributeJsonMixin
from stock_market.core import OHLC, OHLCFetcher, Ticker

logger = get_logger(__name__)


class ProxyOHLCFetcher(OHLCFetcher, SingleAttributeJsonMixin):
    JSON_ATTRIBUTE_NAME = "api_url"
    JSON_ATTRIBUTE_TYPE = "string"

    def __init__(self, api_url):
        super().__init__("proxy")
        self.api_url = api_url

    async def fetch_ohlc(self, requests):
        print(
            {
                "requests": [
                    {
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                        "ticker": ticker.symbol,
                    }
                    for start_date, end_date, ticker in requests
                ]
            }
        )
        async with aiohttp.ClientSession() as client:
            response = await client.post(
                self.api_url,
                json={
                    "requests": [
                        {
                            "start_date": start_date.isoformat(),
                            "end_date": end_date.isoformat(),
                            "ticker": ticker.to_json(),
                        }
                        for start_date, end_date, ticker in requests
                    ]
                },
            )
        ohlc_data = await response.json()
        for ticker, ohlc in ohlc_data.items():
            yield Ticker.from_json(ticker), OHLC.from_json(ohlc)

    def __eq__(self, other):
        if not isinstance(other, ProxyOHLCFetcher):
            return False
        return self.api_url == other.api_url
