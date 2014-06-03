#!/usr/bin/python

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as intgr
import mpl_toolkits.mplot3d as mp3d  # marked as unused, but projection='3d' not found without it
from math import pi, sin, cos, sqrt, asin


def sq(num):
    """calculate aquare of num"""
    return num * num


def rotvec(base, angles):
    """Take a base vector and rotate it by the angles given for each axis
    in the angles vector. The angles are expected to be in th 1 to -1 range
    with 1 meaning 180deg counter-clockwise and -1 meaning 180deg clockwise"""
    # print base, angles
    rotangles = np.array([asin(angles[0]) * 2, asin(angles[1]) * 2, asin(angles[2]) * 2])
    rotmx = ([1, 0, 0], [0, cos(rotangles[0]), -sin(rotangles[0])], [0, sin(rotangles[0]), cos(rotangles[0])])
    rotmy = ([cos(rotangles[1]), 0, sin(rotangles[1])], [0, 1, 0], [-sin(rotangles[1]), 0, cos(rotangles[1])])
    rotmz = ([cos(rotangles[2]), -sin(rotangles[2]), 0], [sin(rotangles[2]), cos(rotangles[2]), 0], [0, 0, 1])

    step1 = np.dot(base, rotmx)
    step2 = np.dot(step1, rotmy)
    step3 = np.dot(step2, rotmz)
    # print step3
    return step3, (rotangles/(2*pi))*360


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
                    data = np.array([float(x) for x in row[2:5]])
                    data[0] = 0
                    data[1] = 0
                    rotdata_.append(data)

            if "AccLin" in row[0]:
                hasaccdata = True
                if hasrotdata:
                    data = np.array([float(x) for x in row[2:5]])
                    data[2] = 0
                    accdata_.append(data)
    return rotdata_, accdata_

def getdatafromlogfile2(filename):
    """Reads in the given log file and returns the contained 3D-vectors from the
    linear Accelerometer and the Rotation data. Discards values as long as not both devices
    are active"""
    gyrdata_ = []
    accdata_ = []
    magdata_ = []
    gpsdata_ = []

    with open(filename, 'r') as csvfile:
        rawdata = csv.reader(csvfile, delimiter='\t', quotechar='"')
        for row in rawdata:
            if "GYR" in row[1]: 
                data = np.array([int(row[0])] + [float(y) for y in row[2:5]])
                gyrdata_.append(data)

            if "ACC" in row[1]:
                data = np.array([int(row[0])] + [float(y) for y in row[2:5]])
                accdata_.append(data)
                    
            if "MAG" in row[1]:
                data = np.array([int(row[0])] + [float(y) for y in row[2:5]])
                magdata_.append(data)
                    
            if "GPS" in row[1]:
                data = np.array([int(row[0])] + [float(y) for y in row[2:5]])
                gpsdata_.append(data)
    return gyrdata_, accdata_, magdata_, gpsdata_


gyrData, accData, magData, gpsData = getdatafromlogfile2("sensorLog.txt")

#veldata = [np.array([0, 0, 0])]
#posdata = [np.array([0, 0, 0])]
#newvel = np.array([0, 0, 0])
#newpos = np.array([0, 0, 0])
#
accarray = np.array(accData)
rotarray = np.array(gyrData)
magarray = np.array(magData)
gpsarray = np.array(gpsData)
#accstatlist = []
#rotdeglist = []
#
#for acc, rot in zip(accarray, rotarray):
#    accstatic, rotdeg = rotvec(acc, rot)
#    accstatlist.append(accstatic)
#    rotdeglist.append(rotdeg)
#accstatarray = np.array(accstatlist)
#rotdegarray = np.array(rotdeglist)
#
#velocityx = intgr.cumtrapz(accstatarray[:, 0], initial=0)
#velocityy = intgr.cumtrapz(accstatarray[:, 1], initial=0)
#velocityz = intgr.cumtrapz(accstatarray[:, 2], initial=0)

#print zip(accstatarray[:, 0], velocityx)


fig = plt.figure()
fig.add_subplot(2,2,1)
plt.title("Acc")
plt.plot(accarray[:, 0], accarray[:, 1], accarray[:, 0], accarray[:, 2], accarray[:, 0], accarray[:, 3])
fig.add_subplot(2,2,2)
plt.title("Gyro")
plt.plot(rotarray[:, 0], rotarray[:, 1], rotarray[:, 0], rotarray[:, 2], rotarray[:, 0], rotarray[:, 3])
fig.add_subplot(2,2,3)
plt.title("Magneto")
plt.plot(magarray[:, 0], magarray[:, 1], magarray[:, 0], magarray[:, 2], magarray[:, 0], magarray[:, 3])
plt.show()

#fig.add_subplot(3,5,2)
#plt.plot(rotarray[:, 0])
#fig.add_subplot(3,5,7)
#plt.plot(rotarray[:, 1])
#fig.add_subplot(3,5,12)
#plt.plot(rotarray[:, 2])
#
#fig.add_subplot(3,5,3)
#plt.plot(rotdegarray[:, 0])
#fig.add_subplot(3,5,8)
#plt.plot(rotdegarray[:, 1])
#fig.add_subplot(3,5,13)
#plt.plot(rotdegarray[:, 2])
#
#fig.add_subplot(3,5,4)
#plt.plot(accstatarray[:, 0])
#fig.add_subplot(3,5,9)
#plt.plot(accstatarray[:, 1])
#fig.add_subplot(3,5,14)
#plt.plot(accstatarray[:, 2])
#
#fig.add_subplot(3,5,5)
#plt.plot(velocityx)
#fig.add_subplot(3,5,10)
#plt.plot(velocityy)
#fig.add_subplot(3,5,15)
#plt.plot(velocityz)


# for x,y,z in zip(velocityx, velocityy, velocityz):
#     print x,y,z
#
#positionx = intgr.cumtrapz(velocityx, initial=0)
#positiony = intgr.cumtrapz(velocityy, initial=0)
#positionz = intgr.cumtrapz(velocityz, initial=0)
#
#
#fig = plt.figure()
## fig.add_subplot(4,1,1)
## plt.plot(rotData)
##
## fig.add_subplot(4,1,2)
## plt.plot(gData)
##
## fig.add_subplot(4,2,1)
## plt.plot(accData)
#
#ax = fig.add_subplot(1, 1, 1, projection='3d')
#ax.scatter(gpsarray[:,1], gpsarray[:,2], gpsarray[:,3])
#
#
#plt.show()
