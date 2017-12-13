#!/usr/bin/python
from src import config

import numpy as np
import cv2
import sys

def readFromVideo(videoID, TRAINING):
    if TRAINING:
        videoDir = config.trainingVideoDir
        listDir = config.trainingListDir
        imageDir = config.trainingImageDir
    else:
        videoDir = config.testVideoDir
        listDir = config.testListDir
        imageDir = config.testImageDir

    cap = cv2.VideoCapture(videoDir + '%d.avi' %(videoID))
    imageList = np.genfromtxt(listDir + '%d.txt' %(videoID), usecols=(1))

    for i in range(len(imageList)):
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, imageList[i])
        ret, img = cap.read()
        cv2.imwrite(imageDir + '%d/%d.jpg' %(videoID, i), img);


if __name__ == "__main__":
    if sys.argv[1] == 'training':
        TRAINING = 1
        numberOfVideos = config.numberOfTrainingVideo
    elif sys.argv[1] == 'test':
        TRAINING = 0
        numberOfVideos = config.numberOfTestVideo

    if config.DEBUG:
        readFromVideo(0, TRAINING)
    else:
        print '#Read from %s video' %(sys.argv[1])
        for i in range(numberOfVideos):
            print ' *Processing video %d' %(i)
            readFromVideo(i, TRAINING)
