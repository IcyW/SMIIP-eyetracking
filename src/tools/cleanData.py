#!/usr/bin/python
from src import config

import numpy as np

def cleanData():
    data = np.genfromtxt(config.videoDir + 'data.txt', skip_header=7, usecols=(0, 4, 5, 6, 7, 8, 9, 10, 11, 12), dtype=None)

    # Convert time strings to second-based
    for row in data:
        splitSec = row[1].split('.')
        dotSecond = round(float(splitSec[1].split('/')[0]) / 30000, 4)

        d, h, m, s = splitSec[0].split(':')
        second = int(h) * 3600 + int(m) * 60 + int(s) + dotSecond

        row[1] = second

    np.savetxt(config.videoDir + 'dataCleaned.txt', data, fmt="%s")


if __name__ == "__main__":
    cleanData()
