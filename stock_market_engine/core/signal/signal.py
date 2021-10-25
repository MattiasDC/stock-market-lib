import datetime
import json

class Signal:
	def __init__(self, name, date):
		self.__name = name
		self.__date = date

	@property
	def name(self):
		return self.__name

	@property
	def date(self):
		return self.__date

	def __str__(self):
		return f"{self.name} ({self.date})"

	def __repr__(self):
		return f"Signal({self.name}, {self.date})"

	def __eq__(self, other):
		if not isinstance(other, Signal):
			return False
		return (self.name, self.date) == (other.name, other.date)

	def to_json(self):
		return json.dumps({"name" : self.name, "date" : json.dumps(self.date, default=datetime.date.isoformat)})

	@staticmethod
	def from_json(json_str):
		json_obj = json.loads(json_str)
		return Signal(json_obj["name"], datetime.date.fromisoformat(json.loads(json_obj["date"])))