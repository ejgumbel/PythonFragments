# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 09:36:18 2016

@author: q0rmcgsk
"""

import os
from os import listdir
from os.path import isfile, join
import re


def remove_ext(s):
    return s[0:-4]


def get_state_code(s):
    return s[0:2]


line_starts = ["Duration: 01d\n", "Duration: 1 days \n", "Duration: 1 days\n", "Duration: 24h\n"]
dupe_header_use = 2 #when the header is duplicated, use which ordered occurrence of it?

working_dir = "D:\\DSOD\\Data\\AMAX_Files"
os.chdir(working_dir)

onlyfiles = [f for f in listdir(working_dir) if isfile(join(working_dir, f))]

# http://stackoverflow.com/questions/2474216/python-to-extract-data-from-a-file

for f in onlyfiles:
    st = get_state_code(f)
    # TODO: add something that checks how many times the duration is in the file because it incorrectly labels
    #  sub-daily. The logic works for 1-day because it's incorrectly labeled for NV and AZ, but when I go to get 1-hour,
    #   I'm going to have to do something totally different. Maybe extract 1-hour only for CA, then swing back to only
    #    do NV and AZ for the first occurrence of 1-day, only if there are two occurrences?
    header_count = 0
    with open(f) as infile:
        for line in infile:
            if line in line_starts:
                header_count = header_count + 1
    g = working_dir + "\\1_day\\" + remove_ext(f) + "_1d.txt"
    with open(f) as infile:
        dupe_header_check = 0
        with open(g, "w") as outfile:
            collector = []
            started = False
            for line in infile:
                if line in line_starts:
                    dupe_header_check = dupe_header_check + 1
                    if dupe_header_check == dupe_header_use or header_count == 1:
                        started = True
                        collector = []
                collector.append(line)
                if line == "\n" and started:
                    for outline in collector[1:]:
                        clean_line = re.sub(' +', '\t', outline.strip())
                        outfile.write(clean_line + '\n')
                    break
