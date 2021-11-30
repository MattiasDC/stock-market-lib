import datetime as dt
import json
import numpy as np
import math
import pandas as pd

from utils.math import sign

from stock_market.core import TimeSeries, Ticker, add_signal, SignalDetector, Sentiment
from .ticker_signal import TickerSignal

class CrossoverSignalDetector(SignalDetector):
	def __init__(self,
				 identifier,
				 name,
				 ticker,
				 responsive_indicator_getter,
				 unresponsive_indicator_getter,
				 sentiment):
		super().__init__(identifier, name)
		self.__ticker = ticker
		self.__responsive_indicator_getter = responsive_indicator_getter
		self.__unresponsive_indicator_getter = unresponsive_indicator_getter
		self.__sentiment = sentiment
		assert sentiment != Sentiment.NEUTRAL

	@property
	def ticker(self):
		return self.__ticker

	def detect(self, from_date, to_date, stock_market, sequence):
		ohlc = stock_market.ohlc(self.ticker)
		assert ohlc is not None
		responsive_values = self.__responsive_indicator_getter(ohlc.close)
		unresponsive_values = self.__unresponsive_indicator_getter(ohlc.close)
		difference = responsive_values.values - unresponsive_values.values
		difference = TimeSeries("difference", pd.concat([ohlc.dates, difference], axis=1, ignore_index=True))
		relevant_differences = difference.time_values.loc[(difference.dates >= (from_date-dt.timedelta(days=1))) &\
													      (difference.dates <= to_date)]

		# Extract all date/values where we crossover
		crossovers_indices = np.sign(relevant_differences.value).diff().ne(0)
		crossovers_indices.iloc[0] = False # not interested in the day before from_date
		for _, date_and_value in relevant_differences.loc[crossovers_indices].iterrows():
			if date_and_value.value > 0 and self.__sentiment == Sentiment.BULLISH:
				sequence = add_signal(sequence, TickerSignal(self.id,
															 self.name,
															 self.__sentiment,
															 self.ticker,
															 date_and_value.date))
			elif date_and_value.value < 0 and self.__sentiment == Sentiment.BEARISH:
				sequence = add_signal(sequence, TickerSignal(self.id,
															 self.name,
															 self.__sentiment,
															 self.ticker,
															 date_and_value.date))
		return sequence

	def __eq__(self, other):
		if not isinstance(other, CrossoverSignalDetector):
			return False
		return (self.ticker,
				self.__responsive_indicator_getter,
				self.__unresponsive_indicator_getter,
				self.__sentiment) ==\
			(other.ticker,
			 other.__responsive_indicator_getter,
			 other.__unresponsive_indicator_getter,
			 other.__sentiment)

	@staticmethod
	def NAME():
		return "Crossover"

	def to_json(self):
		return json.dumps({"id" : self.id,
						   "name" : self.name,
						   "ticker" : self.ticker.to_json(),
						   "responsive_indicator_getter" : 
					   			{"name" : self.__responsive_indicator_getter.__class__.__name__,
					   			 "config" : self.__responsive_indicator_getter.to_json()},
						   "unresponsive_indicator_getter" : 
						   		{"name" : self.__unresponsive_indicator_getter.__class__.__name__,
					   			 "config" : self.__unresponsive_indicator_getter.to_json()},
						   "sentiment" : self.__sentiment.to_json()})

	@staticmethod
	def from_json(json_str, indicator_factory):
		json_obj = json.loads(json_str)
		responsive_json = json_obj["responsive_indicator_getter"]
		unresponsive_json = json_obj["unresponsive_indicator_getter"]
		return CrossoverSignalDetector(json_obj["id"],
									   json_obj["name"],
									   Ticker.from_json(json_obj["ticker"]),
									   indicator_factory.create(responsive_json["name"], responsive_json["config"]),
									   indicator_factory.create(unresponsive_json["name"], unresponsive_json["config"]),
									   Sentiment.from_json(json_obj["sentiment"]))

	@staticmethod
	def json_schema():
		return { "type": "object",
  				 "properties": {
    			 	"id": { "type": "integer" },
    			 	"name" : { "type" : "string" },
    			 	"ticker" : { "type" : "string" },
    			 	"responsive_indicator_getter" : 
    			 		{ "type" : "object",
    			 		  "properties" : {
    			 		  	"name" : { "type" : "string" },
    			 		  	"config" : { "type" : "string" },
    			 		   }
    			 		},
    			 	"unresponsive_indicator_getter" :
    			 		{ "type" : "object",
    			 		  "properties" : {
    			 		  	"name" : { "type" : "string" },
    			 		  	"config" : { "type" : "string" }
    			 		  }
    			 		},
    			 	"sentiment" : { "type" : "string"}
    			 }
    		   }