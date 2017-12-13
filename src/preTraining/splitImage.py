#!/usr/bin/python
from src import config

import numpy as np
import sys
import shutil


def splitImage(videoID):
    imageList = np.genfromtxt(config.trainingListDir + '%d_crop.txt' %(videoID), dtype=str)

    # train/val ratio
    ratio = 0.75

    numberOfImg = len(imageList)
    numberOfTrain = int(round(numberOfImg * ratio))
    #print numberOfImg, numberOfTrain

    np.random.shuffle(imageList)

    np.save(config.trainingListDir + '%d_shuffled.npy' %(videoID), imageList)
    np.savetxt(config.trainingListDir + '%d_train.txt' %(videoID), imageList[:numberOfTrain], fmt='%s')
    np.savetxt(config.trainingListDir + '%d_val.txt' %(videoID), imageList[numberOfTrain:], fmt='%s')

    for i in range(numberOfTrain):
        #print i, imageList[i][0]
        shutil.copy(config.trainingImageDir + '%d_crop/%s.jpg' %(videoID, imageList[i][0]), config.trainingImageDir + '%d_train' %(videoID))
    for i in range(numberOfTrain, numberOfImg):
        #print i, imageList[i][0]
        shutil.copy(config.trainingImageDir + '%d_crop/%s.jpg' %(videoID, imageList[i][0]), config.trainingImageDir + '%d_val' %(videoID))


if __name__ == "__main__":
    if config.DEBUG:
        splitImage(0)
        splitImage(1)
    else:
        print '#Split image'
        for i in range(config.numberOfTrainingVideo + 1):
            print ' *Processing video %d' %(i)
            splitImage(i)
