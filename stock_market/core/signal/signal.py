import datetime
import json

from .sentiment import Sentiment

class Signal:
	def __init__(self, identifier, name, sentiment, date):
		self.__id = identifier
		self.__name = name
		self.__sentiment = sentiment
		self.__date = date

	@property
	def name(self):
		return self.__name

	@property
	def id(self):
		return self.__id

	@property
	def sentiment(self):
		return self.__sentiment

	@property
	def date(self):
		return self.__date

	def __str__(self):
		return repr(self)

	def __repr__(self):
		return f"Signal(id={self.id}, name={self.name}, sentiment={self.sentiment}, date={self.date})"

	def __eq__(self, other):
		if not isinstance(other, Signal):
			return False
		assert (self.id == other.id) == (self.name == other.name)
		assert (self.id != other.id) or (self.sentiment == other.sentiment)

		return (self.id, self.date) == (other.id, other.date)

	def to_json(self):
		return json.dumps({"id" : self.id,
						   "name" : self.name,
						   "sentiment" : json.dumps(self.sentiment.value),
						   "date" : json.dumps(self.date, default=datetime.date.isoformat)})

	@staticmethod
	def from_json(json_str):
		json_obj = json.loads(json_str)
		return Signal(json_obj["id"],
					  json_obj["name"],
					  Sentiment(json.loads(json_obj["sentiment"])),
					  datetime.date.fromisoformat(json.loads(json_obj["date"])))

	@staticmethod
	def json_schema():
		return { "type": "object",
  				 "properties": {
    			 	"id": { "type": "integer" },
    			 	"name" : { "type" : "string" },
    			 	"sentiment" : { "type" : "string"},
    			 	"date" : {"type" : "string", "format" : "date"}
    			 }
    		   }