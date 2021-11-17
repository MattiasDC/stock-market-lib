import dateparser
import datetime
import json
from pydantic import BaseModel, Json, constr
from typing import List
from stock_market_engine.api.config import get_settings
from stock_market_engine.core import Engine
from stock_market_engine.core import StockMarket
from stock_market_engine.core import Ticker

class TickerModel(BaseModel):
	symbol : constr(max_length=get_settings().max_ticker_symbol_length)

	def create(self):
		return Ticker(self.symbol)

class StockMarketModel(BaseModel):
	start_date: datetime.date
	tickers: List[TickerModel]

	def create(self):
		return StockMarket(self.start_date, [ticker.create() for ticker in self.tickers])

class SignalModel(BaseModel):
	name : str
	config : Json

	def create(self, factory):
		return factory.create(self.name, self.config)

class SignalsModel(BaseModel):
	signals: List[SignalModel]

	def create(self, factory):
		return [signal_config.create(factory) for signal_config in self.signals]

class EngineModel(BaseModel):
	stock_market: StockMarketModel
	signals: SignalsModel

	def create(self, stock_updater_factory, signal_detector_factory):
		sm = self.stock_market.create()
		signal_detectors = self.signals.create(signal_detector_factory)
		stock_updater = stock_updater_factory.create(get_settings().stock_updater, None)
		return Engine(sm, stock_updater, signal_detectors)