#!/usr/bin/python
from src import config

import numpy as np
import cv2

def writeToVideo(videoID):
    cap = cv2.VideoCapture(config.testVideoDir + '%d.avi' %(videoID))
    writer = cv2.VideoWriter(config.videoDir + 'prediction/%d.avi' %(videoID), cv2.cv.FOURCC('M','J','P','G'), 28, (config.videoWidth, config.videoHeight))

    imageList = np.genfromtxt(config.testListDir + '%d_briefPrediction.txt' %(videoID), dtype=int, usecols=(0))
    mapping = np.genfromtxt(config.testListDir + '%d.txt' %(videoID), dtype=int)
    data = np.genfromtxt(config.testVideoDir + '%d.txt' %(videoID), usecols=(1))

    j = 0
    for i in range(len(data)):
        if j < len(imageList) and mapping[imageList[j]][1] == i:
            img = cv2.imread(config.testImageDir + '%d_prediction/%d.jpg' %(videoID, imageList[j]))
            for dur in range(28):
                writer.write(img)
            j += 1
        else:
            cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, i)
            ret, img = cap.read()
            writer.write(img)

    cap.release()
    writer.release()


if __name__ == "__main__":
    if config.DEBUG:
        writeToVideo(1)
    else:
        print '#Write to video'
        for i in range(config.numberOfTestVideo):
            print ' *Processing video %d' %(i)
            writeToVideo(i)
