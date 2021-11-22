import datetime
import json

class Signal:
	def __init__(self, identifier, name, date):
		self.__id = identifier
		self.__name = name
		self.__date = date

	@property
	def name(self):
		return self.__name

	@property
	def id(self):
		return self.__id

	@property
	def date(self):
		return self.__date

	def __str__(self):
		return repr(self)

	def __repr__(self):
		return f"Signal(id={self.id}, name={self.name}, date={self.date})"

	def __eq__(self, other):
		if not isinstance(other, Signal):
			return False
		assert (self.id == other.id) == (self.name == other.name)

		return (self.id, self.date) == (other.id, other.date)

	def to_json(self):
		return json.dumps({"id" : self.id,
						   "name" : self.name,
						   "date" : json.dumps(self.date, default=datetime.date.isoformat)})

	@staticmethod
	def from_json(json_str):
		json_obj = json.loads(json_str)
		return Signal(json_obj["id"],
					  json_obj["name"],
					  datetime.date.fromisoformat(json.loads(json_obj["date"])))