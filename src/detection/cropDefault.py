#!/usr/bin/python
from src import config

import numpy as np
import cv2
import PIL
from PIL import Image, ImageDraw

def cropDefault(videoID):
	imageList = np.genfromtxt(config.testListDir + '%d.txt' %(videoID), usecols=(1), dtype=int)
	data = np.genfromtxt(config.testVideoDir + '%d.txt' %(videoID), usecols=(2, 3))

	deltaList = [32, 48, 64]

	for i in range(len(imageList)):
		img = Image.open(config.testImageDir + '%d/%d.jpg' %(videoID, i))
		index = imageList[i]
		x = data[index][0]
		y = data[index][1]

		for delta in deltaList:
			deltaX = delta
			deltaY = delta

			# Determine the boundary
			if x - deltaX >= 0:
				left = x - deltaX
			else:
				left = 0

			if y - deltaY >= 0:
				up = y - deltaY
			else:
				up = 0

			if x + deltaX <= config.videoWidth:
				right = x + deltaX
			else:
				right = config.videoWidth

			if y + deltaY <= config.videoHeight:
				down = y + deltaY
			else:
				down = config.videoHeight

			# Crop out the ROI(region of interest)
			cropped = img.crop([left, up, right, down])
			#cropped.show()

			cropped.save(config.testImageDir + '%d_crop/%d/%d.jpg' %(videoID, delta, i))


if __name__ == "__main__":
	if config.DEBUG:
		cropDefault(0)
		cropDefault(1)
	else:
		print '#Crop default'
		for i in range(config.numberOfTestVideo):
			print ' *Processing video %d' %(i)
			cropDefault(i)
