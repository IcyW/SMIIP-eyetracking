#!/usr/bin/python
from src import config

import numpy as np
import cv2

def splitVideo(category):
    cap = cv2.VideoCapture(config.videoDir + 'scene.mov')
    data = np.genfromtxt(config.videoDir + 'dataCleaned.txt', dtype=str)

    videoSeq = np.genfromtxt(config.videoDir + category + 'VideoSeq.txt', usecols=(0, 1), dtype=int)

    #for i in range(1):
    for i in range(len(videoSeq)):
        print ' *Processing video %d' %(i)

        writer = cv2.VideoWriter(config.videoDir + '%s/%d.avi' %(category, i), cv2.cv.FOURCC('M','J','P','G'), 28, (config.videoWidth, config.videoHeight))

        stFrame = videoSeq[i][0] - 1
        edFrame = videoSeq[i][1] - 1

        subData = data[stFrame:edFrame]
        np.savetxt(config.videoDir + '%s/%d.txt' %(category, i), subData, fmt='%s')

        for i in range(stFrame, edFrame):
            curTime = float(data[i][1]) * 1000
            cap.set(cv2.cv.CV_CAP_PROP_POS_MSEC, curTime)
            ret, img = cap.read()
            writer.write(img)

        """
        ret, img = cap.read()
        cv2.imshow('img', img)
        cv2.waitKey(0)
        """

        writer.release()

    cap.release()

if __name__ == "__main__":
    categories = ['training', 'test']
    for category in categories:
        print '#Split %s videos' %(category)
        splitVideo(category)
