import time
import json
import urllib2
from datetime import datetime
from dateutil import tz

def getSunsetTime():
    data = json.load(urllib2.urlopen('https://api.sunrise-sunset.org/json?lat=43.6109200&lng=3.8772300&date=today'))
    sunset = data["results"]["sunset"]
    if sunset[1] == ":":
        sunset = "0" + sunset
    from_zone = tz.gettz('UTC')
    to_zone = tz.tzlocal()
    sunset = datetime.strptime(sunset, "%I:%M:%S %p")
    utc = sunset.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return "%d h %d min" % (central.hour, central.minute)
