import json

from stock_market.core import TimeSeries

class Identity:
	def __call__(self, series : TimeSeries):
		return series

	def __eq__(self, other):
		return isinstance(other, Identity)
		
	def __str__(self):
		return f"Identity"

	def to_json(self):
		return json.dumps({})

	@staticmethod
	def from_json(json_str):
		return Identity()

	@staticmethod
	def json_schema():
		return {}