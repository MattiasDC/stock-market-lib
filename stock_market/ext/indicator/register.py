from stock_market.ext.indicator import MovingAverage, ExponentialMovingAverage

def register_indicator_factories(factory):
	factory.register(ExponentialMovingAverage.__name__,
					 ExponentialMovingAverage.from_json,
					 ExponentialMovingAverage.json_schema())
	factory.register(MovingAverage.__name__,
					 MovingAverage.from_json,
					 MovingAverage.json_schema())
	return factory