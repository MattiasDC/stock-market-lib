import datetime
from fastapi import FastAPI, Request
from .models import EngineModel, TickerModel
from stock_market_engine.api.redis import init_redis_pool
from stock_market_engine.core.engine import Engine
from stock_market_engine.core.ticker import Ticker
import uuid

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis_pool()

@app.post("/create")
async def create_engine(engine_config: EngineModel):
	engine = engine_config.create()
	engine = json_decode(json_encode(engine), Engine)
	random_id = str(uuid.uuid4())

	await app.state.redis.set(random_id, json_encode(engine))
	return random_id

async def get_engine(engine_id):
	engine_json = await app.state.redis.get(str(engine_id))
	return json_decode(engine_json, Engine)

@app.get("/getdate/{engine_id}")
async def get_date(engine_id : uuid.UUID):
	engine = await get_engine(engine_id)
	return engine.stock_market.date

async def storeTemporary(o, redis):
	random_id = str(uuid.uuid4())
	await app.state.redis.set(random_id, json_encode(o), datetime.timedelta(minutes=1))
	return random_id

@app.get("/ticker/{engine_id}/{ticker_id}")
async def get_ticker_data_id(engine_id : uuid.UUID, ticker_id : str):
	engine = await get_engine(engine_id)
	ohlc = engine.stock_market.ohlc(Ticker(ticker_id))
	random_id = await storeTemporary(ohlc, app.state.redis)
	return random_id

@app.get("/signals/{engine_id}")
async def get_signals_id(engine_id : uuid.UUID):
	engine = await get_engine(engine_id)
	random_id = await storeTemporary(engine.signals, app.state.redis)
	return random_id

@app.post("/update/{engine_id}")
async def update_engine(engine_id : uuid.UUID, date : datetime.date):
	engine = await get_engine(engine_id)
	engine.update(date)
	await app.state.redis.set(random_id, json_encode(engine))