import datetime
from fastapi import FastAPI, Request, Response
from http import HTTPStatus
import uuid

from .models import EngineModel, TickerModel
from .config import get_settings
from stock_market_engine.api.redis import init_redis_pool
from stock_market_engine.common.factory import Factory
from stock_market_engine.api.engine import Engine
from stock_market_engine.core import Ticker
from stock_market_engine.ext.signal import register_signal_detector_factories 
from stock_market_engine.ext.updater import register_stock_updater_factories 

app = FastAPI()

def get_signal_detector_factory():
	return register_signal_detector_factories(Factory())

def get_stock_updater_factory():
	return register_stock_updater_factories(Factory())

async def store_temporary(o):
	if o is None:
		return None
	random_id = str(uuid.uuid4())
	await app.state.redis.set(random_id, o.to_json(), get_settings().redis_temporary_expiration_time)
	return random_id

async def store_engine(engine, engine_id):
	await app.state.redis.set(engine_id, engine.to_json(), get_settings().redis_engine_expiration_time)

@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis_pool()

@app.post("/create")
async def create_engine(engine_config: EngineModel):
	engine = engine_config.create(get_stock_updater_factory(), get_signal_detector_factory())
	random_id = str(uuid.uuid4())

	await store_engine(engine, random_id)
	return random_id

async def get_engine(engine_id):
	engine_json = await app.state.redis.get(str(engine_id))
	return Engine.from_json(engine_json, get_stock_updater_factory(), get_signal_detector_factory())

@app.get("/getdate/{engine_id}")
async def get_date(engine_id : uuid.UUID):
	engine = await get_engine(engine_id)
	return engine.stock_market.date

@app.get("/getstartdate/{engine_id}")
async def get_start_date(engine_id : uuid.UUID):
	engine = await get_engine(engine_id)
	return engine.stock_market.start_date

@app.get("/tickers/{engine_id}")
async def get_tickers(engine_id : uuid.UUID):
	engine = await get_engine(engine_id)
	return [ticker.symbol for ticker in engine.stock_market.tickers]

@app.get("/ticker/{engine_id}/{ticker_id}")
async def get_ticker_data_id(engine_id : uuid.UUID, ticker_id : str):
	engine = await get_engine(engine_id)
	ohlc = engine.stock_market.ohlc(Ticker(ticker_id))
	random_id = await store_temporary(ohlc)
	if random_id is None:
		return Response(status_code=HTTPStatus.NO_CONTENT.value)
	return random_id

@app.get("/signals/{engine_id}")
async def get_signals_id(engine_id : uuid.UUID):
	engine = await get_engine(engine_id)
	random_id = await store_temporary(engine.signals)
	if random_id is None:
		return Response(status_code=HTTPStatus.NO_CONTENT.value)
	return random_id

@app.post("/addticker/{engine_id}/{ticker_id}")
async def add_ticker(engine_id : uuid.UUID, ticker_id : str):
	engine = await get_engine(engine_id)
	ticker = Ticker(ticker_id)
	if ticker in engine.stock_market.tickers:
		return Response(status_code=HTTPStatus.NO_CONTENT.value)

	engine = Engine(engine.stock_market.add_ticker(ticker),
					engine.stock_market_updater,
					engine.signal_detectors)
	new_engine_id = str(uuid.uuid4())
	await store_engine(engine, new_engine_id)
	return new_engine_id

@app.post("/removeticker/{engine_id}/{ticker_id}")
async def remove_ticker(engine_id : uuid.UUID, ticker_id : str):
	engine = await get_engine(engine_id)
	ticker = Ticker(ticker_id)
	if ticker not in engine.stock_market.tickers:
		return Response(status_code=HTTPStatus.NO_CONTENT.value)

	engine = Engine(engine.stock_market.remove_ticker(ticker),
					engine.stock_market_updater,
					engine.signal_detectors)
	new_engine_id = str(uuid.uuid4())
	await store_engine(engine, new_engine_id)
	return new_engine_id

@app.post("/update/{engine_id}")
async def update_engine(engine_id : uuid.UUID, date : datetime.date):
	engine = await get_engine(engine_id)
	engine.update(date)
	await store_engine(engine, str(engine_id))