import datetime
from datetime import date

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)
d = date.today()
next_wednesday = next_weekday(d, 2).isoformat()