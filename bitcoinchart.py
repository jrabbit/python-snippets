#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygooglechart import Chart
from pygooglechart import SimpleLineChart
from pygooglechart import Axis
from subprocess import *
import platform
import os

max_y = 2000
# Chart size of 200x125 pixels and specifying the range for the Y axis
chart = SimpleLineChart(500, 250, y_range=[0, max_y])
# grep khash ~/.bitcoin/debug.log

if platform.system() == 'Linux':
    home = os.path.expanduser('~') 
    log = os.path.join(home, '.bitcoin', 'debug.log')
elif platform.system() == 'Darwin':
    home = os.path.expanduser('~') 
    log = os.path.join(home, 'Library', 'Application Support', 'Bitcoin', 'debug.log')
elif platform.system() == 'Windows':
    log = os.path.join(os.environ['appdata'], 'Bitcoin', 'debug.log')
else:
    home = os.path.expanduser('~') 
    log = os.path.join(home, '.bitcoin', 'debug.log')

debug = open(log)
data = []
for line in debug:
    if 'khash' not in line:
        continue
    #print line.split()
    data.append(int(line.split()[-2]))
    #07/19/2010 13:05 hashmeter      3 CPUs   1466 khash/s
    # Date time hashmeter #cpus hash/s
left_axis = range(0, max_y + 1, 500)
left_axis[0] = ''
chart.set_axis_labels(Axis.LEFT, left_axis)
chart.add_data(data)
chart.download('khash.png')
