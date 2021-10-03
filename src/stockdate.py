from datetime import date, timedelta


class StockDate:
    """
    This class encapsulates the concept of a day for stock trading
    """

    def __init__(self, this_date: date):
        self._date = this_date

    @property
    def year(self):
        return self._date.year

    @property
    def month(self):
        return self._date.month

    @property
    def day(self):
        return self._date.day

    def ago_days(self, num_days):
        return StockDate(self._date - timedelta(days=num_days))

    @property
    def yyyy_mm_dd(self) -> str:
        return f"{self.year}-{self.month}-{self.day}"
