#!/usr/bin/python
from src import config

import PIL
from PIL import Image
from PIL import ImageEnhance
from random import randint
from random import uniform
import numpy as np


def augment(videoID):
    imageList = np.genfromtxt(config.trainingListDir + '%d_train.txt' %(videoID), dtype=None)

    lowThreshold = 0.5
    highThreshold = 1.5
    ratio = 1.0 / 3
    halfRatio = ratio / 2

    numberOfVar = 4

    augF = open(config.trainingListDir + '%d_trainAug.txt' %(videoID), 'w')

    for item in imageList:
        img = Image.open(config.trainingImageDir + '%d_train/%s.jpg' %(videoID, item[0]))
        augF.write("%s.jpg %d\n" %(item[0], item[1]))
        
        for idx in range(numberOfVar):
            colorDlt = uniform(lowThreshold, highThreshold)
            contrastDlt = uniform(lowThreshold, highThreshold)
            brightnessDlt = uniform(lowThreshold, highThreshold)

            enhancer = ImageEnhance.Color(img)
            tmp = enhancer.enhance(colorDlt)
            enhancer = ImageEnhance.Contrast(tmp)
            tmp = enhancer.enhance(contrastDlt)
            enhancer = ImageEnhance.Brightness(tmp)
            tmp = enhancer.enhance(brightnessDlt)

            newName = '%s_%d.jpg' %(item[0], idx)
            tmp.save(config.trainingImageDir + '/%d_train/%s' %(videoID, newName))
            augF.write("%s %d\n" %(newName, item[1]))
        
        curWidth, curHeight = img.size
        coor = [(0, 0, (1 - ratio) * curWidth, (1 - ratio) * curHeight), (ratio * curWidth, 0, curWidth, (1 - ratio) * curHeight), (0, ratio * curHeight, (1 - ratio) * curWidth, curHeight), (ratio * curWidth, ratio * curHeight, curWidth, curHeight), (halfRatio * curWidth, halfRatio * curHeight, (1 - halfRatio) * curWidth, (1 - halfRatio) * curHeight)]
        
        for idx in range(len(coor)):
            tmp = img.crop(coor[idx])
            newName = '%s_partial_%d.jpg' %(item[0], idx)
            tmp.save(config.trainingImageDir + '/%d_train/%s' %(videoID, newName))
            augF.write("%s %d\n" %(newName, item[1]))


if __name__ == "__main__":
    if config.DEBUG:
        augment(0)
        augment(1)
    else:
        print '#Augment train'
        for i in range(config.numberOfTrainingVideo + 1):
            print ' *Processing video %d' %(i)
            augment(i)
