# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 10:57:57 2019

@author: q0hecgsk
"""


import urllib.request
from urllib.request import HTTPError
from datetime import datetime
from datetime import timedelta
import os

start = datetime(2015, 6, 26, 13, 0)
end = datetime(2015, 6, 26, 17, 0)
hour = timedelta(hours=1)

missing_dates = []
fallback_to_radaronly = True #Enables a post-processing step that will go through the list of missing dates for gage-corrected
############################# and tries to go get the radar-only values if they exist.

destination = "C:/Data/Meteorology/QPE/test"

date = start

while date <= end:
    url = "http://mtarchive.geol.iastate.edu/{:04d}/{:02d}/{:02d}/mrms/ncep/GaugeCorr_QPE_01H/GaugeCorr_QPE_01H_00.00_{:04d}{:02d}{:02d}-{:02d}0000.grib2.gz".format(
        date.year, date.month, date.day, date.year, date.month, date.day, date.hour)
    filename = url.split("/")[-1]
    try:
        fetched_request = urllib.request.urlopen(url)
    except HTTPError as e:
        missing_dates.append(date)
    else:
        f = open(destination + os.sep + filename, 'wb')
        f.write(fetched_request.read())
    finally:
        date += hour
f.close()

if fallback_to_radaronly:
    radar_also_missing = []
    for date in missing_dates:
        url = "http://mtarchive.geol.iastate.edu/{:04d}/{:02d}/{:02d}/mrms/ncep/RadarOnly_QPE_01H/RadarOnly_QPE_01H_00.00_{:04d}{:02d}{:02d}-{:02d}0000.grib2.gz".format(
            date.year, date.month, date.day, date.year, date.month, date.day, date.hour)
        filename = url.split("/")[-1]
        try:
            fetched_request = urllib.request.urlopen(url)
        except HTTPError as e:
            radar_also_missing.append(date)
        else:
            f = open(destination + os.sep + filename, 'wb')
            f.write(fetched_request.read())
f.close()