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

working_dir = "D:\\DSOD\\Data\\AMAX_Files"
os.chdir(working_dir)

ftp_path = "https://hdsc.nws.noaa.gov/pub/hdsc/data/_TimeSeries_stations/"
station_file = pd.read_csv("D:\\DSOD\\Data\\ca_by_div.csv")

onlyfiles = [f for f in listdir(working_dir) if isfile(join(working_dir, f))]
stations_downloaded = [remove_ext(s) for s in onlyfiles]

#for station in station_file["Station_ID"]:
for idx, row in station_file.iterrows():
    station = row["Station_ID"]
    state_code = row["State"]
    file_name = state_code + "_" + station + "_ams.txt"
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
        pass
        #print(station)

