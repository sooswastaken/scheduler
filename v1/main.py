import datetime
import enum
import random


class DayTypes(enum.Enum):
    RED = "RED"
    BLACK = "BLACK"
    WEEKEND = "WEEKEND"


class Periods(enum.Enum):
    FIRST = "FIRST"
    SECOND = "SECOND"
    THIRD = "THIRD"
    FOURTH = "FOURTH"
    FIFTH = "FIFTH"
    SIXTH = "SIXTH"
    SEVENTH = "SEVENTH"
    EIGHTH = "EIGHTH"


class Schedule:
    def __init__(self):
        # known_date is september 1st, 12AM UTC, and it is when the schedule is known
        self.known_date = datetime.datetime(2020, 9, 1, 0, 0, 0, 0)
        self.black_day_times = {
            # black days: second period, fourth period, sixth period, eighth period
            # second period is from 8:10AM to 9:37AM
            "second_period": (datetime.time(8, 10), datetime.time(9, 37)),
            # fourth period is from 9:45AM to 11:12AM
            "fourth_period": (datetime.time(9, 45), datetime.time(11, 12)),
            # sixth period is from 11:20AM to 1:19PM
            "sixth_period": (datetime.time(11, 20), datetime.time(13, 19)),
            # eighth period is from 1:27PM to 2:55PM
            "eighth_period": (datetime.time(13, 27), datetime.time(15, 55)),
        }
        self.red_day_times = {
            # red days: first period, third period, fifth period, seventh period
            # first period is from 8:10AM to 9:37AM
            "first_period": (datetime.time(8, 10), datetime.time(9, 37)),
            # third period is from 9:45AM to 11:12AM
            "third_period": (datetime.time(9, 45), datetime.time(11, 12)),
            # fifth period is from 11:20AM to 1:19PM
            "fifth_period": (datetime.time(11, 20), datetime.time(13, 19)),
            # seventh period is from 1:27PM to 2:55PM
            "seventh_period": (datetime.time(13, 27), datetime.time(15, 55)),
        }

        self.stinger_times = {
            # Stinger is during fourth period on black days
            # The first half of stinger is from 9:45 to 10:25AM
            # The second half of stinger is from 10:33PM to 11:12AM
            "first_half": (datetime.time(9, 45), datetime.time(10, 25)),
            "second_half": (datetime.time(10, 33), datetime.time(11, 12)),
        }

    def get_day_difference(self, date) -> int:
        return (date - self.known_date).days

    def even_or_odd_day(self, date) -> DayTypes:
        if self.get_day_difference(date) % 2 == 0:
            return DayTypes.BLACK
        else:
            return DayTypes.RED

    def is_transitioning_between_periods(self, time, red_or_black_day) -> bool:
        pass

    def current_class(self, *, testing_time=None) -> str:
        current_time = datetime.datetime.now().time()
        if testing_time:
            current_time = testing_time
        day_type = self.even_or_odd_day(datetime.datetime.now())
        if day_type == DayTypes.RED:
            for period in self.red_day_times:
                if self.red_day_times[period][0] <= current_time <= self.red_day_times[period][1]:
                    return period
        else:
            for period in self.black_day_times:
                if self.black_day_times[period][0] <= current_time <= self.black_day_times[period][1]:
                    # Check if the period is a stinger period
                    if period == "fourth_period":
                        # Check which half of the stinger period the current time is in
                        # if it is the first half, return "stinger_first_half"
                        # if it is the second half, return "stinger_second_half"
                        if self.stinger_times["first_half"][0] <= current_time <= self.stinger_times["first_half"][1]:
                            return "stinger_first_half"
                        elif self.stinger_times["second_half"][0] <= current_time <= self.stinger_times["second_half"][1]:
                            return "stinger_second_half"
                    return period
                else:
                    print(f"{current_time} is not in {period}")


# Create a testing instance of the Schedule class
test_schedule = Schedule()
print(test_schedule.current_class())
