import ephem
from pytz import utc, timezone
from datetime import datetime, timedelta
from copy import copy

######################################################################
## Hoa: 13.04.2018 Version 1 : sun_1.py
######################################################################
# Calculates sunset, sunrise as well moonrise and moonset
#
# New /Changes:
# ----------------------------------------------------------------------
#
# 13.04.2018 : first implemented
#
######################################################################
# Koordinaten iHomelab: 47.014956; 8.305175
#
# Quellen:
#  - https://oneau.wordpress.com/2010/07/04/astrometry-in-python-with-pyephem/
#  - http://rhodesmill.org/pyephem/quick.html
#  - https://michelanders.blogspot.ch/2011/01/moon-phases-with-pyephem.html
#
######################################################################
sun = ephem.Sun()
moon = ephem.Moon()
est = timezone('EST')


def get_observer():
    location = ephem.Observer()
    location.lon = '-47.014956'      # [degrees]
    location.lat = '8.305175'       # [degrees]
    location.elevation = 446        # elevation above sea level [meters]
    location.horizon = '-0:34'
    location.date = ephem.Date(datetime.utcnow())

    return location


def sunrise(observer, date):
    observer.date = date.astimezone(utc)
    return observer.next_rising(sun).datetime().replace(tzinfo=utc)


def sunrises(observer, start_date, offset_seconds=0):
    # offset negative before, positive after
    current_date = copy(start_date)
    while 1:
        yield sunrise(observer, current_date) + timedelta(seconds=offset_seconds)
        current_date = current_date + timedelta(days=1)


def sunset(observer, date):
    observer.date = date.astimezone(utc)
    return observer.next_setting(sun).datetime().replace(tzinfo=utc)


def sunsets(observer, start_date, offset_seconds=0):
    # offset negative before, positive after
    current_date = copy(start_date)
    while 1:
        yield sunset(observer, current_date) + timedelta(seconds=offset_seconds)
        current_date = current_date + timedelta(days=1)


def moonset(observer, date):
    observer.date = date.astimezone(utc)
    return observer.next_setting(moon).datetime().replace(tzinfo=utc)


def moonsets(observer, start_date, offset_seconds=0):
    # offset negative before, positive after
    current_date = copy(start_date)
    while 1:
        yield moonset(observer, current_date) + timedelta(seconds=offset_seconds)




def main():
    try:
        current_date = datetime.now()
        tomorrow = current_date + timedelta(days=1)
        my_utc = datetime.utcnow()
        print('Tomorrow is: {}'.format(current_date))
        obs = get_observer()
        print('Next Sunrise @ {}'.format(sunrise(obs,my_utc)))



    except Exception as e:
      print(' MAIN: Error in main: ' + str(e))


if __name__ == '__main__':
    main()