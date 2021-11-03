FROM python:3.9-slim-buster

RUN mkdir -p /app

# set working directory
WORKDIR /app

COPY pyproject.toml .
COPY setup.cfg .
COPY setup.py .
COPY ./stock_market_engine ./stock_market_engine

RUN pip install . --no-cache-dir --use-feature=in-tree-build

EXPOSE 8000
CMD ["uvicorn", "stock_market_engine.api.main:app", "--host", "0.0.0.0", "--lifespan=on", "--use-colors", "--reload"]