# config.py
# Global variables

import numpy as np
import logging
import sys

DEBUG = 0
if DEBUG:
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
else:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

videoName = 'ADOS_0'

dataDir = 'data/'

videoDir = dataDir + 'video/' + videoName + '/'
trainingVideoDir = videoDir + 'training/'
testVideoDir = videoDir + 'test/'

imageDir = dataDir + 'image/' + videoName + '/'
trainingImageDir = imageDir + 'training/'
testImageDir = imageDir + 'test/'

imageListDir = dataDir + 'imageList/' + videoName + '/'
trainingListDir = imageListDir + 'training/'
testListDir = imageListDir + 'test/'
detectionListDir = imageListDir + 'detection/'

numberOfTrainingVideo = 14
numberOfTestVideo = 9

videoWidth = 640
videoHeight = 480

labels = ['Baby', 'Rabbit', 'RedToy', 'BlueToy', 'ToyGuy', 'FireEngine', 'Truck', 'Book', 'Plate', 'Chestbox', 'FoodContainer', 'Ball', 'Cup', 'Jar', 'Other']

labels_to_ind = dict(zip(labels, xrange(len(labels))))
ind_to_labels = dict(zip(xrange(len(labels)), labels))

defaultBBoxSide = 48
deviationX = 16
deviationY = 16

DETECTION = 1