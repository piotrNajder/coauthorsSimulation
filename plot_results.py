import matplotlib.pyplot as plt
import numpy as np
import glob as gl

import math

from simu_utils import natural_keys, readConfigFile

### parse the config file

worldConfig = readConfigFile("input.xml")
n_test = int(worldConfig.get("n_test"))

## Process the histogram data first

histList = gl.glob("./results/hist*.dat")
histList.sort(key = natural_keys)

histArrays = list()

for histFile in histList:
    with open(histFile, "r") as f:        
        lines = f.readlines()
        vals = np.zeros(len(lines))
        indexes = np.zeros(len(lines))
        for i, line in enumerate(lines):
            line = line.replace("\n", "")
            indexes[i] = int(line.split(" ")[0])
            vals[i] = float(line.split(" ")[1])
        
        histArrays.append((indexes, vals))

axesX = int(math.sqrt(len(histArrays)))
axesY = axesX
if axesY * axesX < len(histArrays):
    axesY += 1

fig, axs = plt.subplots(axesX, axesY)

fig.suptitle('Distibution of numbers of coauthors for given steps of simulation')

histIndex = 0
for i in range(0, axesX):
    for j in range(0, axesY):
        rects = axs[i, j].bar(histArrays[histIndex][0], histArrays[histIndex][1], 0.2)
        s = histIndex * n_test
        if s == 0: s = 1
        axs[i, j].set_title("s = {}".format(s))
        histIndex += 1
        if histIndex >= len(histArrays): break
    if histIndex >= len(histArrays): break

plt.subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9,
        top = 0.85, wspace = 0.8, hspace = 0.8)

plt.show()

### Avarage number of coauthors across the simulation

avgs = list()
with open("./results/w.dat") as f:
    lines = f.readlines()

    indexes = np.zeros(len(lines), dtype = np.int)
    vals = np.zeros(len(lines), dtype = float)

    for i, line in enumerate(lines):
        index = int(line.split(" ")[0])
        if index == 0: index = 1
        val = float(line.split(" ")[1])
        avgs.append((index, val))

indexes = np.array(list([idx[0] for idx in avgs]))
vals = np.array(list([idx[1] for idx in avgs]))

fig, ax = plt.subplots()
ax.scatter(indexes, vals)

z = np.polyfit(indexes, vals, 3)
p = np.poly1d(z)
plt.plot(indexes, p(indexes), "r--")

plt.show()

###  Distribution of credits and agents quality across simulation time

filesList = gl.glob("./results/agentStats*.dat")
filesList.sort(key = natural_keys)

creditsArrays = list()
qualitiesArrays = list()
import pdb
for asFile in filesList:
    with open(asFile, "r") as f:        
        lines = f.readlines()
        crs = np.zeros(len(lines))
        qals = np.zeros(len(lines))
        for i, line in enumerate(lines):
            #pdb.set_trace()
            vals = line.split(" ")
            crs[i] = float(vals[1])
            qals[i] = float(vals[2])
        
        creditsArrays.append(crs)
        qualitiesArrays.append(qals)

axesX = int(math.sqrt(len(creditsArrays)))
axesY = axesX
if axesY * axesX < len(creditsArrays):
    axesY += 1

fig, axs = plt.subplots(axesX, axesY)

fig.suptitle('Distibution of credits for given steps of simulation')

crsIndex = 0
for i in range(0, axesX):
    for j in range(0, axesY):
        bins = (int(np.ceil(max(creditsArrays[crsIndex]))) - int(np.floor(min(creditsArrays[crsIndex])))) * 10
        s = crsIndex * n_test
        if s == 0: s = 1

        axs[i, j].hist(creditsArrays[crsIndex], bins = bins)        
        axs[i, j].set_title("s = {}".format(s))
        crsIndex += 1
        if crsIndex >= len(creditsArrays): break
    if crsIndex >= len(creditsArrays): break

plt.subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9,
        top = 0.85, wspace = 0.8, hspace = 0.8)

plt.show()

axesX = int(math.sqrt(len(qualitiesArrays)))
axesY = axesX
if axesY * axesX < len(qualitiesArrays):
    axesY += 1

fig, axs = plt.subplots(axesX, axesY)

fig.suptitle('Distibution of quality for given steps of simulation')

qalsIndex = 0
for i in range(0, axesX):
    for j in range(0, axesY):
        bins = (int(np.ceil(max(qualitiesArrays[qalsIndex]))) - int(np.floor(min(qualitiesArrays[qalsIndex])))) * 10
        s = qalsIndex * n_test
        if s == 0: s = 1

        axs[i, j].hist(qualitiesArrays[qalsIndex], bins = bins)        
        axs[i, j].set_title("s = {}".format(s))
        qalsIndex += 1
        if qalsIndex >= len(qualitiesArrays): break
    if qalsIndex >= len(qualitiesArrays): break

plt.subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9,
        top = 0.85, wspace = 0.8, hspace = 0.8)

plt.show()





