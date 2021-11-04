FROM python:3.9-slim-buster

RUN mkdir -p /app

# set working directory
WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip

COPY setup.py .
COPY pyproject.toml .
COPY setup.cfg .

COPY ./stock_market_engine ./stock_market_engine

RUN pip install -e . --no-cache-dir

EXPOSE 8000
CMD ["uvicorn", "stock_market_engine.api.main:app", "--host", "0.0.0.0", "--lifespan=on", "--use-colors", "--reload"]