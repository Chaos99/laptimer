#!/usr/bin/python

import csv
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as mp3d  #marked as unused, but projection='3d' not found without it
from math import pi, sin, cos


def rotvec(base, angles):
    """Take a base vector and rotate it by the angles given for each axis
    in the angles vector. The angles are expected to be in th 1 to -1 range
    with 1 meaning 180deg counter-clockwise and -1 meaning 180deg clockwise"""
    rotangles = pi * angles
    rotmx = ([1, 0, 0], [0, cos(rotangles[0]), -sin(rotangles[0])], [0, sin(rotangles[0]), cos(rotangles[0])])
    rotmy = ([cos(rotangles[1]), 0, sin(rotangles[1])], [0, 1, 0], [-sin(rotangles[1]), 0, cos(rotangles[1])])
    rotmz = ([cos(rotangles[2]), -sin(rotangles[2]), 0], [sin(rotangles[2]), cos(rotangles[2]), 0], [0, 0, 1])

    step1 = np.dot(base, rotmx)
    step2 = np.dot(step1, rotmy)
    step3 = np.dot(step2, rotmz)
    return step3


def getdatafromlogfile(filename):
    """Reads in the given log file and returns the contained 3D-vectors from the
    linear Accelerometer and the Rotation data. Discards values as long as not both devices
    are active"""
    rotdata_ = []
    accdata_ = []

    with open(filename, 'r') as csvfile:
        rawdata = csv.reader(csvfile, delimiter=',', quotechar='"')
        hasaccdata = False
        hasrotdata = False
        for row in rawdata:
            if "RotVec" in row[0]:
                hasrotdata = True
                if hasaccdata:
                    rotdata_.append(np.array([float(x) for x in row[2:5]]))

            if "AccLin" in row[0]:
                hasaccdata = True
                if hasrotdata:
                    accdata_.append(np.array([float(x) for x in row[2:5]]))
    return rotdata_, accdata_


rotData, accData = getdatafromlogfile("sensoduino.txt")

posData = [np.array([0, 0, 0])]

for acc, rot in zip(accData, rotData):
    oldPos = posData[-1]
    newPos = np.add(oldPos, rotvec(acc, rot))
    posData.append(newPos)

apos = np.array(posData)

fig = plt.figure()
# ax = fig.add_subplot(4,1,1)
# plt.plot(rotData)
#
# ax = fig.add_subplot(4,1,2)
# plt.plot(gData)
#
# ax = fig.add_subplot(4,2,1)
# plt.plot(accData)

ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.scatter(apos[:, 0], apos[:, 1], apos[:, 2])


plt.show()
