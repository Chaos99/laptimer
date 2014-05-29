#!/usr/bin/python

import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import pi, sin, cos

def rotVec( base, angles):
    """Take a base vector and rotate it by the angles given for each axis
    in the angles vector. The angles are expected to be in th 1 to -1 range
    with 1 meaning 180deg counter-clockwise and -1 meaning 180deg clockwise"""
    radAngles = pi * angles
    rotMx = ([1, 0, 0], [0, cos(radAngles[0]), -sin(radAngles[0])], [0, sin(radAngles[0]), cos(radAngles[0])])
    rotMy = ([cos(radAngles[1]), 0, sin(radAngles[1])], [0, 1, 0], [-sin(radAngles[1]), 0, cos(radAngles[1])])
    rotMz = ([cos(radAngles[2]), -sin(radAngles[2]), 0], [sin(radAngles[2]), cos(radAngles[2]), 0], [0, 0, 1])

    step1 = np.dot(base, rotMx)
    step2 = np.dot(step1, rotMy)
    step3 = np.dot(step2, rotMz)
    return step3

rotData = []
gData = []
accData = []

with open("sensoduino.txt", 'r') as csvfile:
    rawData = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in rawData:
        if "RotVec" in row[0]:
            rotData.append(np.array([float(x) for x in row[2:5]]))
        if "Gravity" in row[0]:
            gData.append(np.array([float(x) for x in row[2:5]]))
        if "AccLin" in row[0]:
            accData.append(np.array([float(x) for x in row[2:5]]))

posData = []
posData.append(np.array([0,0,0]))

for acc, rot in zip(accData, rotData):
    oldPos = posData[-1]
    newPos = np.add(oldPos, rotVec(acc, rot)) #add rotational transform here
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

ax = fig.add_subplot(1,1,1, projection='3d')
ax.scatter(apos[:, 0], apos[:, 1], apos[:, 2])


plt.show()
