import os
from functools import cache
from pydantic import AnyUrl, BaseSettings
from stock_market_engine.api.utils import get_logger

logger = get_logger(__name__)

class Settings(BaseSettings):
    redis_url: AnyUrl = os.environ.get("REDIS_URL", "redis://redis")
    redis_port: int = os.getenv("REDIS_PORT", 6379)
    redis_db: int = os.getenv("REDIS_DB", 0)
    stock_updater: str = os.getenv("STOCK_UPDATER", "yahoo")

@cache
def get_settings() -> BaseSettings:
    logger.info("Loading config settings from the environment...")
    return Settings()