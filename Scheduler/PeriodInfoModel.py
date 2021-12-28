class PeriodInfoModel:
    def __init__(self, time_total, time_left, day_type, current_period):
        self.time_total = time_total
        self.time_left = time_left
        self.day_type = day_type
        self.current_period = current_period

    def json(self):
        return {
            "total_period_time_in_seconds": self.time_total.seconds,
            "total_period_left_time_in_seconds": self.time_left.seconds,
            "day_type": self.day_type.value,
            "current_period": self.current_period.value
        }
