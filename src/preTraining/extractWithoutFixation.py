#!/usr/bin/python
from src import config

import logging
import cv2
import sys

def extractFrame(videoID):
    # Extract the frame every 10/28 seconds
    interval = 10

    cap = cv2.VideoCapture(config.trainingVideoDir + '%d.avi' %(videoID))
    length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    with open(config.trainingListDir + '%d.txt' %(videoID), 'w') as f:
        num = 0
        for i in range(0, length, interval):
            cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, i)
            ret, img = cap.read()
            cv2.imwrite(config.trainingImageDir + '%d/%d.jpg' %(videoID, num), img);
            f.write('%d %05d\n' %(num, i))
            num += 1


if __name__ == "__main__":
    if config.DEBUG:
        extractFrame(0)
        extractFrame(1)
    else:
        print '#Extract frame'
        for i in range(config.numberOfTrainingVideo):
            print ' *Processing video %d' %(i)
            extractFrame(i)
