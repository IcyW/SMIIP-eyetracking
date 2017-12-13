#!/usr/bin/python
from src import config

import numpy as np
import logging
from collections import Counter


def count():
    trainList= np.genfromtxt(config.trainingListDir + 'allTrain.txt', dtype=int, usecols=(1))
    valList = np.genfromtxt(config.trainingListDir + 'allVal.txt', dtype=int, usecols=(1))
    trainCounter = Counter(trainList)
    valCounter = Counter(valList)

    logging.info('The number of training images in each category is:')
    for key in config.ind_to_labels:
        if key in trainCounter:
            logging.info('%s %d' %(config.ind_to_labels[key], trainCounter[key]))
        else:
            logging.info('%s %d' %(config.ind_to_labels[key], 0))

    logging.info('The number of test images in each category is:')
    for key in config.ind_to_labels:
        if key in valCounter:
            logging.info('%s %d' %(config.ind_to_labels[key], valCounter[key]))
        else:
            logging.info('%s %d' %(config.ind_to_labels[key], 0))

if __name__ == "__main__":
    count()
