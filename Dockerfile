FROM python:3.9-buster

RUN mkdir -p /app

# set working directory
WORKDIR /app

COPY pyproject.toml .
COPY setup.cfg .

RUN python -m pip install --no-cache-dir --upgrade pip

COPY . .
RUN pip install .

EXPOSE 8000
CMD ["uvicorn", "stock_market_engine.api.main:app", "--host", "0.0.0.0", "--lifespan=on", "--use-colors", "--reload"]