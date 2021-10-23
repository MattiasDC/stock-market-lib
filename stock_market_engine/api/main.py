from fastapi import FastAPI, Request
import jsonpickle
from .models import EngineConfig
from stock_market_engine.api.redis import init_redis_pool
import uuid

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.redis = await init_redis_pool()


@app.post("/createengine")
async def create_engine(engine_config: EngineConfig):
	engine = engine_config.create()
	random_id = str(uuid.uuid4())

	await app.state.redis.set(random_id, jsonpickle.encode(engine))
	return {"id" : random_id}

@app.get("/getdate/{engine_id}")
async def get_date(engine_id : uuid.UUID):
	engine_json = await app.state.redis.get(str(engine_id))
	engine = jsonpickle.decode(engine_json)
	return engine.stock_market.date