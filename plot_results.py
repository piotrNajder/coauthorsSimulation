import matplotlib.pyplot as plt
import numpy as np
import glob as gl

import math

from simu_utils import natural_keys

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

histIndex = 0
for i in range(0, axesX):
    for j in range(0, axesY):
        rects = axs[i, j].bar(histArrays[histIndex][0], histArrays[histIndex][1], 0.2)
        histIndex += 1
        if histIndex >= len(histArrays): break
    if histIndex >= len(histArrays): break
plt.show()

a = "dupa"




