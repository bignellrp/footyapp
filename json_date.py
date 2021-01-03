# Find the date for next wednesday
import datetime 
from datetime import date
from json import dumps
import sys
sys.dont_write_bytecode = True
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)
d = date.today()
next_wednesday = next_weekday(d, 0) # 0 = Monday, 1=Tuesday, 2=Wednesday...
next_wednesday = (dumps(next_wednesday, default=json_serial))