from enum import Enum
import json

class Sentiment(Enum):
    NEUTRAL = "NEUTRAL"
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"

    def to_json(self):
    	return json.dumps(self.value)

    @staticmethod
    def from_json(json_str):
    	return Sentiment(json.loads(json_str))

    @staticmethod
    def json_schema():
    	return { "type" : "string"}