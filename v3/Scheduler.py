# Scheduler, a way to know what period it is, and how much time is left in said period.

import time
import datetime
import enum


class DayTypes(enum.Enum):
    # Type of day it is. EVEN_DAY, ODD_DAY, WEEKEND, HOLIDAY, TWO_HOUR_EARLY_RELEASE
    EVEN_DAY = "EVEN_DAY"
    ODD_DAY = "ODD_DAY"
    WEEKEND = "WEEKEND"
    HOLIDAY = "HOLIDAY"
    TWO_HOUR_EARLY_RELEASE = "TWO_HOUR_EARLY_RELEASE"


class TimeModel:
    def __init__(self, period, day_type, time_left, total_time) -> None:
        self.period = period
        self.day_type = day_type
        self.time_left = time_left
        self.total_time = total_time



class PeriodTypes(enum.Enum):
    # Types of periods. From First period to Eighth period.
    # On even days, fourth period is the called "STINGER" period.
    BEFORE_SCHOOL = "BEFORE_SCHOOL"
    FIRST_PERIOD = "FIRST_PERIOD"
    SECOND_PERIOD = "SECOND_PERIOD"
    THIRD_PERIOD = "THIRD_PERIOD"
    FOURTH_PERIOD = "FOURTH_PERIOD"
    # Stingers are the fourth period on even days.
    # The first half of stinger is 40 minutes, the second half is 39 minutes.
    STINGER_FIRST_HALF = "STINGER_FIRST_HALF"
    STINGER_SECOND_HALF = "STINGER_SECOND_HALF"
    FIFTH_PERIOD = "FIFTH_PERIOD"
    SIXTH_PERIOD = "SIXTH_PERIOD"
    SEVENTH_PERIOD = "SEVENTH_PERIOD"
    EIGHTH_PERIOD = "EIGHTH_PERIOD"
    AFTER_SCHOOL = "AFTER_SCHOOL"


class EvenDayPeriodTimes(enum.Enum):
    # Times for the periods on even days.
    # Times are set as when the period ends.
    # On even days, the periods are:
    # BEFORE SCHOOL, SECOND PERIOD, STINGER PERIODS, SIXTH PERIOD, EIGHTH PERIOD
    # The transition times are when students transition from one period to the next, consisting of 8 minutes.
    BEFORE_SCHOOL = datetime.time(hour=8, minute=2)
    SECOND_PERIOD_TRANSITION = datetime.time(hour=8, minute=10)
    SECOND_PERIOD = datetime.time(hour=9, minute=37)
    # After second period is fourth period, but on even days, it is called stinger, and is separated into two halves.
    STINGER_FIRST_HALF_TRANSITION = datetime.time(hour=9, minute=45)
    STINGER_FIRST_HALF = datetime.time(hour=10, minute=25)
    STINGER_SECOND_HALF_TRANSITION = datetime.time(hour=10, minute=33)
    STINGER_SECOND_HALF = datetime.time(hour=11, minute=12)
    # Sixth period is two hours long, as it is when students have class for 90 minutes, and lunch for 30 minutes.
    # Transitioning between lunches is also factored into the length of sixth period.
    SIXTH_PERIOD_TRANSITION = datetime.time(hour=11, minute=20)
    SIXTH_PERIOD = datetime.time(hour=13, minute=19)
    EIGHTH_PERIOD_TRANSITION = datetime.time(hour=1, minute=27)
    EIGHTH_PERIOD = datetime.time(hour=14, minute=55)


class OddDayPeriodTimes(enum.Enum):
    # Times for the periods on odd days.
    # Times are set as when the period ends.
    # On odd days, the periods are:
    # BEFORE SCHOOL, FIRST PERIOD, THIRD PERIOD, FIFTH PERIOD,SEVENTH PERIOD
    # The transition times are when students transition from one period to the next, consisting of 8 minutes.
    BEFORE_SCHOOL = datetime.time(hour=8, minute=2)
    FIRST_PERIOD_TRANSITION = datetime.time(hour=8, minute=10)
    FIRST_PERIOD = datetime.time(hour=9, minute=37)
    THIRD_PERIOD_TRANSITION = datetime.time(hour=9, minute=45)
    THIRD_PERIOD = datetime.time(hour=11, minute=12)
    FIFTH_PERIOD_TRANSITION = datetime.time(hour=11, minute=20)
    FIFTH_PERIOD = datetime.time(hour=13, minute=19)
    SEVENTH_PERIOD_TRANSITION = datetime.time(hour=1, minute=27)
    SEVENTH_PERIOD = datetime.time(hour=14, minute=55)


class Scheduler:
    # Scheduler class.
    # This class is used to determine what period it is, and how much time is left in said period.
    # Periods are determined by the time it is, and the day it is.
    # Odd and every days are determined by a subtraction of days from a known date, and the current date
    # The known date is september 1st, and it is a even day.
    # Since we know this, we know that september 1st is a even day, and so on.
    KNOWN_DATE = datetime.datetime(year=2021, month=9, day=1)
    KNOWN_DATE_DAY_TYPE = DayTypes.EVEN_DAY

    # TODO: Add a way to determine holidays, and two hour early releases
    def get_day_type(self, date):
        # Returns the day type of the given date. Currently, can only be even, odd, or a weekend

        # Check if it is a weekend
        if date.weekday() > 5:
            return DayTypes.WEEKEND

        # Other wise, check if it is an even or odd day.

        # Subtract the date from the known date.
        days = (date - self.KNOWN_DATE).days
        return DayTypes.EVEN_DAY if days % 2 == 0 else DayTypes.ODD_DAY

    def get_even_day_period_time(self, date):
        for times in EvenDayPeriodTimes:
            if date.time() < times.value:
                return times
        return None

    def get_odd_day_period_time(self, date):
        for times in OddDayPeriodTimes:
            if date.time() < times.value:
                return times
        return None

    def get_time(self, date):
        # Check if its a odd, even, or weekend day.
        day_type = self.get_day_type(date)
        if day_type == DayTypes.EVEN_DAY:
            return self.get_even_day_period_time(date)
        elif day_type == DayTypes.ODD_DAY:
            return self.get_odd_day_period_time(date)

    def get_time_left(self, date):
        # Get the time left in the current period.
        # This is done by subtracting the current time from the time of the next period.
        # If the current time is less than the next period, then the time left is 0.
        period = self.get_time(date)
        if period is None:
            return None

        # Convert the period to a datetime.datetime object
        period_time = datetime.datetime.combine(date, period.value)
        # Convert the current time to a datetime.datetime object
        current_time = datetime.datetime.combine(date, date.time())

        # Get the time left in the period
        time_left = period_time - current_time
        return time_left, period_time

    def get_info(self, date):
        # This method returns a TimeModel object, which contains the current period, the type of day, and the time left in the period.
        time_left, total_time = self.get_time_left(date)
        # getattr the period from EvenDayPeriodTimes or OddDayPeriodTimes to PeriodTypes
        day_type = self.get_day_type(date).value
        period = getattr(PeriodTypes, self.get_time(date).name).value
        return TimeModel(period, day_type, time_left, total_time)



