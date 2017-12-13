#!/usr/bin/python
from src import config

import numpy as np
import cv2
import math
import PIL
from PIL import Image, ImageDraw
import csv
import sys


def defaultCrop(fixationX, fixationY):
    # Create a 96x96 crop by default
    if fixationX - config.defaultBBoxSide >= 0:
        left = fixationX - config.defaultBBoxSide
    else:
        left = 0
            
    if fixationY - config.defaultBBoxSide >= 0:
        top = fixationY - config.defaultBBoxSide
    else:
        top = 0
        
    if fixationX + config.defaultBBoxSide <= config.videoWidth:
        right = fixationX + config.defaultBBoxSide
    else:
        right = config.videoWidth

    if fixationY + config.defaultBBoxSide <= config.videoHeight:
        bottom = fixationY + config.defaultBBoxSide
    else:
        bottom = config.videoHeight
    
    return [left, top, right, bottom]


def isInBBox(fixationX, fixationY, left, right, top, bottom):
    """
    # Hard boundary
    if fixationX >= left and fixationX <= right and fixationY >= top and fixationY <= bottom:
        return True
    else:
        return False
    """

    # Allow a little deviation. TO TUNE
    if fixationX >= left - config.deviationX and fixationX <= right + config.deviationX and fixationY >= top - config.deviationY and fixationY <= bottom + config.deviationY:
        return True
    else:
        return False


def cropBoundingBox(videoID, DETECTION):
    imageList = np.genfromtxt(config.testListDir + '%d.txt' %(videoID), usecols=(1), dtype=int)
    data = np.genfromtxt(config.testVideoDir + '%d.txt' %(videoID), usecols=(2, 3))

    # Each image is separated by an empty line
    with open(config.testListDir +  '%d_detection.txt' %(videoID), 'r') as f:
        reader = csv.reader(f)
        detection = list(reader)
        detectionLen = len(detection)

    lowerRGB = np.array([60, 30, 30], dtype='uint8')
    upperRGB = np.array([150, 60, 80], dtype='uint8')
    pixelThreshold = 2000
    areaThreshold = 80000

    curRow = 0
    with open(config.testListDir +  '%d_crop.txt' %(videoID), 'w') as f:
        for i in range(len(imageList)):
            #print 'Processing image: %d, %d' %(i, imageList[i])
            img = Image.open(config.testImageDir + '%d/%d.jpg' %(videoID, i))
            #img.show()

            fixationX = data[imageList[i]][0]
            fixationY = data[imageList[i]][1]

            if DETECTION:
                # Initialize the region
                rLeft = fixationX
                rRight = fixationX
                rTop = fixationY
                rBottom = fixationY
                flag = 0

                if detection[curRow] == []:
                    coor = defaultCrop(fixationX, fixationY)
                    rLeft = coor[0]
                    rTop = coor[1]
                    rRight = coor[2]
                    rBottom = coor[3]
                    curRow += 1
                else:
                    for j in range(curRow + 1, detectionLen):
                        if detection[j] == []:
                            break
                    subData = detection[curRow:j]
                    curRow = j + 1

                    for j in range(len(subData)):
                        info = subData[j][0].split(' ')
                        prob = info[0]
                        left = int(info[1])
                        top = int(info[2])
                        right = int(info[3])
                        bottom = int(info[4])

                        if (right - left) * (bottom - top) > areaThreshold:
                            continue

                        # The fixation point is in the bounding box
                        if isInBBox(fixationX, fixationY, left, right, top, bottom):
                            if flag == 0:
                                rLeft = left
                                rRight = right
                                rTop = top
                                rBottom = bottom
                                flag = 1
                            else:
                                # If the region is contained in the current bounding box, then do nothing.
                                if left <= rLeft and right >= rRight and top <= rTop and bottom >= rBottom:
                                    continue
                                # If current bounding box is contained in the region, then choose the current bbox as the new region.
                                if left >= rLeft and right <= rRight and top >= rTop and bottom <= rBottom:
                                    rLeft = left
                                    rRight = right
                                    rTop = top
                                    rBottom = bottom
                                    continue
                                
                                # Else decide which region it belongs to based on how far it is deviated from the center of each region.
                                centerX = (left + right) / 2
                                centerY = (top + bottom) / 2
                                rCenterX = (rLeft + rRight) / 2
                                rCenterY = (rTop + rBottom) / 2

                                dist = math.pow(centerX - fixationX, 2) + math.pow(centerY - fixationY, 2)
                                distR = math.pow(rCenterX - fixationX, 2) + math.pow(rCenterY - fixationY, 2)

                                #print 'Center: %d, %d' %(centerX, centerY)
                                #print 'rCenter: %d, %d' %(rCenterX, rCenterY)
                                #print 'Dist: %d, %d' %(dist, distR)

                                # If the fixaiton point is closer to the current bounding box, then choose the current bbox as the new region.
                                if dist < distR:
                                    rLeft = left
                                    rRight = right
                                    rTop = top
                                    rBottom = bottom
                                elif dist > distR:
                                    continue
                                else:
                                    if left < rLeft:
                                        rLeft = left
                                    if right > rRight:
                                        rRight = right
                                    if top < rTop:
                                        rTop = top
                                    if bottom > rBottom:
                                        rBottom = bottom 

                                # And there are many other options out there:
                                # 1. Use the merged region.
                                # 2. Use the intersection.

                    if rLeft == rRight or rTop == rBottom:
                        coor = defaultCrop(fixationX, fixationY)
                        rLeft = coor[0]
                        rTop = coor[1]
                        rRight = coor[2]
                        rBottom = coor[3]
            else:
                coor = defaultCrop(fixationX, fixationY)
                rLeft = coor[0]
                rTop = coor[1]
                rRight = coor[2]
                rBottom = coor[3]

            #print i, rLeft, rRight, rTop, rBottom
            cropped = img.crop([rLeft, rTop, rRight, rBottom])
            pixels = np.array(cropped)
            mask = cv2.inRange(pixels, lowerRGB, upperRGB)
            count = np.count_nonzero(mask)
            #print i, count
            if count > pixelThreshold:
                continue

            f.write('%d %d %d %d %d\n' %(i, rLeft, rTop, rRight, rBottom))
            #cropped.show()
            cropped.save(config.testImageDir + '%d_crop/%d.jpg' %(videoID, i))


if __name__ == "__main__":
    if config.DEBUG:
        cropBoundingBox(0, config.DETECTION)
        #cropBoundingBox(1)
    else:
        print '#Crop BoundingBox'
        for i in range(config.numberOfTestVideo):
            print ' *Processing video %d' %(i)
            cropBoundingBox(i, config.DETECTION)
