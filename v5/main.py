from Scheduler.Scheduler import Scheduler
import datetime

s = Scheduler()
days = (datetime.datetime.now() - Scheduler.KNOWN_DATE).days
print(days)
