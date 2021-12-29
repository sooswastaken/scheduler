import datetime
from .DayTypes import DayTypes
from .EVEN_DAY_PERIOD_TYPES import EVEN_DAY_PERIOD_TYPES
from .ODD_DAY_PERIOD_TYPES import ODD_DAY_PERIOD_TYPES
from .PeriodInfoModel import PeriodInfoModel
import aiosqlite


class Scheduler:
    KNOWN_DATE = datetime.datetime(year=2021, month=9, day=1)

    def __init__(self):
        self.db = None

    async def format_stinger_period(self, date, half):
        days = (date - self.KNOWN_DATE).days
        if not self.db:
            self.db = await aiosqlite.connect('database.db')



    def get_day_type(self, date):
        # Returns the day type of the given date. Currently, can only be even, odd, or a weekend

        # Check if it is a weekend
        if date.weekday() > 5:
            return DayTypes.WEEKEND

        # Other wise, check if it is an even or odd day.

        # Subtract the date from the known date.
        days = (date - self.KNOWN_DATE).days
        return DayTypes.EVEN_DAY if days % 2 == 0 else DayTypes.ODD_DAY

    async def get_period_info(self, date):
        # Returns two values: the total time of the period, and the time remaining in the period.
        time_left = None
        time_total = None
        current_period = None

        # Get the day type
        day_type = self.get_day_type(date)

        if day_type == DayTypes.EVEN_DAY:
            # Determine what period it currently is
            for period in EVEN_DAY_PERIOD_TYPES:
                if date.time() < period.value["end"]:
                    current_period = period.value["type"]
                    # Convert the period end time to a datetime.datetime object
                    end_time = datetime.datetime.combine(date, period.value["end"])
                    time_left = end_time - date
                    previous_period = getattr(EVEN_DAY_PERIOD_TYPES, period.value["previous"].name)
                    previous_period_end = datetime.datetime.combine(date, previous_period.value["end"])
                    time_total = end_time - previous_period_end
                    break
        if day_type == DayTypes.ODD_DAY:
            # Determine what period it currently is
            for period in ODD_DAY_PERIOD_TYPES:
                if date.time() < period.value["end"]:
                    current_period = period.value["type"]
                    # Convert the period end time to a datetime.datetime object
                    end_time = datetime.datetime.combine(date, period.value["end"])
                    time_left = end_time - date
                    previous_period = getattr(ODD_DAY_PERIOD_TYPES, period.value["previous"].name)
                    previous_period_end = datetime.datetime.combine(date, previous_period.value["end"])
                    time_total = end_time - previous_period_end
                    break
        return PeriodInfoModel(time_total, time_left, day_type, current_period)
