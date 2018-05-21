#!/usr/bin/python


# DIESE VARIANTE ist naeher am korrekten SONNEN-AUFGANG !


# https://github.com/mdoege/PyoRhythm/blob/master/conky/rise.py
# http://stackoverflow.com/questions/2637293/calculating-dawn-and-sunset-times-using-pyephem
# http://dateandtime.info/de/citysunrisesunset.php?id=2657896
# sonnen position: http://www.solartopo.com/sonnenumlaufbahn.htm

# Print Sun/Moon rise and set times for today

import ephem
import datetime
from pytz import timezone
import pytz

berlin = timezone('Europe/Zurich')
utc = pytz.utc

dat = datetime.datetime.now()
loc1 = berlin.localize(datetime.datetime(dat.year, dat.month, dat.day, 0, 0, 0))
loc2 = loc1.astimezone(utc)

#Make an observer
fred      = ephem.Observer()

#PyEphem takes and returns only UTC times
fred.date = ephem.Date(loc2)

fred.lon  = '47.014956'  # [degrees]
fred.lat  = '8.305175'   # [degrees]

#Elevation in metres
fred.elev = 446

#To get U.S. Naval Astronomical Almanac values, use these settings
fred.pressure= 0
fred.horizon = '-0:34'

sunrise=fred.next_rising(ephem.Sun()) #Sunrise
sunset =fred.next_setting(ephem.Sun()) #Sunset

moonrise=fred.next_rising(ephem.Moon())
moonset =fred.next_setting(ephem.Moon())

#We relocate the horizon to get twilight times
fred.horizon = '-6' #-6=civil twilight, -12=nautical, -18=astronomical
beg_twilight=fred.next_rising(ephem.Sun(), use_center=True) #Begin civil twilight
end_twilight=fred.next_setting(ephem.Sun(), use_center=True) #End civil twilight

fmt = "%H:%M"
fmt2 = '%Y-%m-%d %H:%M:%S'

# diese Variante Stimmt nicht !!
print('Date and Time: {}'.format(dat.strftime(fmt2)))
sr,ss=ephem.localtime(sunrise).strftime(fmt),ephem.localtime(sunset).strftime(fmt)
print('%10s ▲%s ▼%s' % ('Sonne:',sr, ss))
bt,et=ephem.localtime(beg_twilight).strftime(fmt),ephem.localtime(end_twilight).strftime(fmt)
print('%10s ▲%s ▼%s' % ('Dämmerung:',bt, et))
mr,ms=ephem.localtime(moonrise).strftime(fmt),ephem.localtime(moonset).strftime(fmt)
print('%10s ▲%s ▼%s' % ('Mond:',mr, ms))

# correcte Variante !!!
o=ephem.Observer()
o.lat='47.014956'
o.long='8.305175'
o.elev = 446
o.pressure= 0
o.horizon = '-0:34'

s=ephem.Sun()
s.compute()
print('\n')
print('Next Sun Rise: {}'.format(ephem.localtime(o.next_rising(s)).strftime(fmt2)))
print('Next Sun Set : {}'.format(ephem.localtime(o.next_setting(s)).strftime(fmt2)))