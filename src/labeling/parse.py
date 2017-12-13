# Ref: https://github.com/tzutalin/ImageNet_Utils

#!/usr/bin/python
from src import config

import xml.etree.ElementTree as ET
from PIL import Image

import sys
import os

def parse(videoID, TRAINING):
    if TRAINING:
        imageDir = config.trainingImageDir
    else:
        imageDir = config.testImageDir

    annotationFiles = []
    for root, dirs, files in os.walk(imageDir + str(videoID)):
        for file in files:
            if file.endswith('.xml'):
                annotationFiles.append(os.path.join(root, file))
    annotationFiles.sort()
    #print annotationFiles

    if TRAINING:
        f = open(config.trainingListDir + '%d_crop.txt' %(videoID), 'w')
    else:
        f = open(config.testListDir + '%d_groundtruth.txt' %(videoID), 'w')

    for xmlfile in annotationFiles:
        xmltree = ET.parse(xmlfile)
        filename = xmltree.find('filename').text
        path = xmltree.find('path').text

        objects = xmltree.findall('object')
        rects = []
        names = []
        for object_iter in objects:
            bndbox = object_iter.find('bndbox')
            rects.append([int(it.text) for it in bndbox])
            names.append(object_iter.find('name').text)
        #print filename, names, rects

        if TRAINING:
            outPath = path.rsplit('/', 1)[0] + '_crop/'
            # Get crop images
            count = 0
            img = Image.open(path)
            for i in range(len(rects)):
                cropImg = img.crop(rects[i])
                outName = '%d_%s_%d' %(videoID, filename, count)
                cropImg.save(outPath + outName + '.jpg')
                count = count + 1
                f.write('%s %d\n' %(outName, config.labels_to_ind[names[i]]))
        else:
            for i in range(len(rects)):
                f.write('%s %d %d %d %d %d %s\n' %(filename, rects[i][0], rects[i][1], rects[i][2], rects[i][3], config.labels_to_ind[names[i]], names[i]))


if __name__ == "__main__":
    if sys.argv[1] == 'training':
        TRAINING = 1
        numberOfVideos = config.numberOfTrainingVideo + 1
    elif sys.argv[1] == 'test':
        TRAINING = 0
        numberOfVideos = config.numberOfTestVideo

    if config.DEBUG:
        parse(0, TRAINING)
        parse(1, TRAINING)
    else:
        print '#Parse %s XMLs' %(sys.argv[1])
        for i in range(numberOfVideos):
            print ' *Processing video %d' %(i)
            parse(i, TRAINING)
