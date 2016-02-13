#!/usr/bin/python

import netTable

import time
import os

nt = netTable.makeNetworkTable('10.16.19.2', 'SmashBoard')
nt.addConnectionListener(netTable.ConnectionListener('/home/ubuntu/Robot2016/connectionLog.txt'))

i = 0
while True:
    nt.putNumber('robotTime', i)
    time.sleep(1)
    i += 1
