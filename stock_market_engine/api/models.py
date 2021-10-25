import dateparser
import datetime
import json
from pydantic import BaseModel, Json, constr
from typing import List
from stock_market_engine.api.config import get_settings
from stock_market_engine.core.engine import Engine
from stock_market_engine.core.stock_market import StockMarket
from stock_market_engine.core.ticker import Ticker
from stock_market_engine.signals.signal_detector_factory import SignalDetectorFactory
from stock_market_engine.updaters.stock_updater_factory import StockUpdaterFactory

class TickerModel(BaseModel):
	symbol : constr(max_length=5)

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

	def create(self):
		return SignalDetectorFactory().create(json.loads(self.json()))

class SignalsModel(BaseModel):
	signals: List[SignalModel]

	def create(self):
		return [signal_config.create() for signal_config in self.signals]

class EngineModel(BaseModel):
	stock_market: StockMarketModel
	signals: SignalsModel

	def __create_stock_updater(self):
		return StockUpdaterFactory().create(get_settings().stock_updater)
	
	def create(self):
		sm = self.stock_market.create()
		signal_detectors = self.signals.create()
		stock_updater = self.__create_stock_updater()
		return 	Engine(sm, stock_updater, signal_detectors)