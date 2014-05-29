#!/usr/bin/python

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as intgr
import mpl_toolkits.mplot3d as mp3d  # marked as unused, but projection='3d' not found without it
from math import pi, sin, cos, sqrt


def sq(num):
    """calculate aquare of num"""
    return num * num


def rotvec(base, angles):
    """Take a base vector and rotate it by the angles given for each axis
    in the angles vector. The angles are expected to be in th 1 to -1 range
    with 1 meaning 180deg counter-clockwise and -1 meaning 180deg clockwise"""
    # print base, angles
    rotangles = pi * angles
    rotmx = ([1, 0, 0], [0, sqrt(1 - sq(rotangles[0])), -rotangles[0]], [0, rotangles[0], sqrt(1 - sq(rotangles[0]))])
    rotmy = ([sqrt(1 - sq(rotangles[1])), 0, rotangles[1]], [0, 1, 0], [-rotangles[1], 0, sqrt(1 - sq(rotangles[1]))])
    #rotmz = ([sqrt(1 - sq(rotangles[1])), -rotangles[1], 0], [0, 1, 0], [-rotangles[1], 0, sqrt(1 - sq(rotangles[1]))])

    #rotmz = rotangles[2]
    if sq(rotangles[2]) > 1:
        print rotangles[2]
    rotmz = ([sqrt(1 - sq(rotangles[2])), -rotangles[2], 0], [rotangles[2], sqrt(1 - sq(rotangles[2])), 0], [0, 0, 1])

    step1 = np.dot(base, rotmx)
    step2 = np.dot(step1, rotmy)
    step3 = np.dot(step2, rotmz)
    # print step3
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

veldata = [np.array([0, 0, 0])]
posdata = [np.array([0, 0, 0])]
newvel = np.array([0, 0, 0])
newpos = np.array([0, 0, 0])

accarray = np.array(accData)
rotarray = np.array(rotData)
accstatlist = []

for acc, rot in zip(accarray, rotarray):
    accstatic = rotvec(acc, rot)
    accstatlist.append(accstatic)
accstatarray = np.array(accstatlist)

velocityx = intgr.cumtrapz(accstatarray[:, 0], initial=0)
velocityy = intgr.cumtrapz(accstatarray[:, 1], initial=0)
velocityz = intgr.cumtrapz(accstatarray[:, 2], initial=0)

print zip(accstatarray[:, 0], velocityx)
fig = plt.figure()
fig.add_subplot(3,4,1)
plt.plot(accarray[:, 0])
fig.add_subplot(3,4,5)
plt.plot(accarray[:, 1])
fig.add_subplot(3,4,9)
plt.plot(accarray[:, 2])

fig.add_subplot(3,4,2)
plt.plot(rotarray[:, 0])
fig.add_subplot(3,4,6)
plt.plot(rotarray[:, 1])
fig.add_subplot(3,4,10)
plt.plot(rotarray[:, 2])

fig.add_subplot(3,4,3)
plt.plot(accstatarray[:, 0])
fig.add_subplot(3,4,7)
plt.plot(accstatarray[:, 1])
fig.add_subplot(3,4,11)
plt.plot(accstatarray[:, 2])

fig.add_subplot(3,4,4)
plt.plot(velocityx)
fig.add_subplot(3,4,8)
plt.plot(velocityy)
fig.add_subplot(3,4,12)
plt.plot(velocityz)


# for x,y,z in zip(velocityx, velocityy, velocityz):
#     print x,y,z

positionx = int.cumtrapz(velocityx, initial=0)
positiony = int.cumtrapz(velocityy, initial=0)
positionz = int.cumtrapz(velocityz, initial=0)


fig = plt.figure()
# fig.add_subplot(4,1,1)
# plt.plot(rotData)
#
# fig.add_subplot(4,1,2)
# plt.plot(gData)
#
# fig.add_subplot(4,2,1)
# plt.plot(accData)

fig.add_subplot(1, 1, 1, projection='3d')
ax.scatter(positionx, positiony, positionz)


plt.show()
