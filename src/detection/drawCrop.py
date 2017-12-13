#!/usr/bin/python
from src import config

import numpy as np
import PIL
from PIL import Image, ImageDraw, ImageFont


def drawFixation(videoID):
    radius = 5

    data = np.genfromtxt(config.testVideoDir + '%d.txt' %(videoID), usecols=(2, 3))
    imageList = np.genfromtxt(config.testListDir + '%d.txt' %(videoID), dtype=int)
    crop = np.genfromtxt(config.testListDir + '%d_crop.txt' %(videoID), dtype=int)

    for i in range(len(crop)):
        index = crop[i][0]
        img = Image.open(config.testImageDir + '%d_detection/%d.jpg' %(videoID, index))
        
        x = data[imageList[index][1]][0]
        y = data[imageList[index][1]][1]
        #print crop[i]

        draw = ImageDraw.Draw(img)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(0, 0, 255, 0))
        draw.line((0, y, config.videoWidth, y), fill=(0, 0, 255, 0), width=3)
        draw.line((x, 0, x, config.videoHeight), fill=(0, 0, 255, 0), width=3)

        for delta in range(5):
            xmin = max(0, crop[i][1] + delta)
            xmax = min(config.videoWidth, crop[i][3] - delta)
            ymin = max(0, crop[i][2] + delta)
            ymax = min(config.videoHeight, crop[i][4] - delta)

            draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 255, 255, 0))

        img.save(config.testImageDir + '%d_detection/%d.jpg' %(videoID, index))


if __name__ == "__main__":
    if config.DEBUG:
        drawFixation(0)
        drawFixation(1)
    else:
        print '#Draw fixation'
        for i in range(config.numberOfTestVideo):
            print ' *Processing video %d' %(i)
            drawFixation(i)
