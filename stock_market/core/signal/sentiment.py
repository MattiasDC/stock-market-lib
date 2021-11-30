from enum import Enum
import json

from stock_market.common.single_attribute_json_mixin import SingleAttributeJsonMixin

class Sentiment(SingleAttributeJsonMixin, Enum):
    @classmethod
    @property
    def JSON_ATTRIBUTE_NAME(cls):
        return "value"

    @classmethod
    @property
    def JSON_ATTRIBUTE_TYPE(cls):
        return "string"

    NEUTRAL = "NEUTRAL"
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"