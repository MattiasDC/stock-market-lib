import datetime as dt


class StockUpdater:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def _get_period(self, stock_market, ohlc, date):
        date = date + dt.timedelta(days=1)
        if ohlc is None:
            return stock_market.start_date, date
        return ohlc.end, date
