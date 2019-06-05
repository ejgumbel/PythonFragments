# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 09:22:04 2016

@author: q0rmcgsk
"""

import os
from os import listdir
from os.path import isfile, join
import urllib
from urllib.error import URLError
import pandas as pd

def remove_ext(s):
    return s[0:-4]

def retrieve_with_timeout(remote_path, file_name, timeout = 60):
    remote_path = ftp_path + file_name
    url_request = urllib.request.urlopen(remote_path, timeout = timeout)
    with open(file_name, "wb") as f:
        try:
            f.write(url_request.read())
        except:
            raise

working_dir = "C:\\Users\\q0hecgsk\\Desktop\\test\\ams"
os.chdir(working_dir)

ftp_path = "ftp://hdsc.nws.noaa.gov/pub/hdsc/data/_TimeSeries_stations/"
station_file = pd.read_csv("C:\\Users\\q0hecgsk\\Desktop\\test\\PrecGageStations_Whittier_100miles_updated.txt")

onlyfiles = [f for f in listdir(working_dir) if isfile(join(working_dir, f))]
#stations_downloaded = [remove_ext(s) for s in onlyfiles]

for station in station_file["Station_ID"]:
    file_name = "CA_" + station + "_ams.txt"
    if file_name in onlyfiles:
        continue
    remote_path = ftp_path + file_name
    try:
        #urllib.request.urlretrieve(remote_path, file_name)
        retrieve_with_timeout(remote_path, file_name)
    except URLError as e:
        print("File not found, skipping...")
        continue
    finally:
        print(station)

