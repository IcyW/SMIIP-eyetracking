#!/usr/bin/python
from src import config

import numpy as np
import logging
import sys

def filterFrame(videoID, TRAINING):
    MODE = 3

    if TRAINING:
        videoDir = config.trainingVideoDir
        listDir = config.trainingListDir
    else:
        videoDir = config.testVideoDir
        listDir = config.testListDir

    if MODE == 1:
        logging.debug('MODE 1')

        # Read data(fixation point and validation info)
        data = np.genfromtxt(videoDir + '%d.txt' %(videoID), usecols=(2, 3, 6))

        # Hyper-parameters
        xThreshold = 20
        yThreshold = 20
        durationThreshold = 8

        # Flag variables
        start = 0
        end = 0
        total = 0

        # Iterate through all the frames and choose the valid frames
        # Method: Comparing with the prevous frame, the movement of the fixation point 
        # is within the predefined threshold
        # Assume that the first frame is valid
        with open(listDir + '%d.txt' %(videoID), 'w') as f:
            for i in range(1, len(data)):
                curData = data[i]

                # If the current fixation is invalid, i.e.,
                # corneal reflection is not detected or fixation point is not in the frame
                if curData[2] == -1000 or\
                curData[0] > config.videoWidth or curData[0] < 0 or\
                curData[1] > config.videoHeight or curData[1] < 0:
                    
                    logging.debug('#Frame %d is invalid' %(i))
                    # If the number of consecutive valid frames > durationThreshold,
                    # we select the middle frame
                    if end - start + 1 >= durationThreshold:
                        f.write('%d %05d\n' %(total, (start + end) / 2))
                        total += 1
                        logging.debug('*Region (%d, %d) is valid, and frame %d is selected.' %(start, end, (start + end) / 2))
                    
                    # Else we abandon the frame and reset the variables
                    else:
                        logging.debug('*Region (%d, %d) is abandoned!' %(start, i))

                    start = i + 1
                    end = i + 1
                    continue
                
                prevData = data[i - 1]
                if abs(curData[0] - prevData[0] < xThreshold) and\
                    abs(curData[1] - prevData[1] < yThreshold):
                    end += 1
                else:
                    logging.debug('#Frame %d is too far away from the previous fixation!' %(i))

                    if end - start + 1 >= durationThreshold:
                        f.write('%d %05d\n' %(total, (start + end) / 2))
                        total += 1
                        logging.debug('*Region (%d, %d) is valid, and frame %d is selected.' %(start, end, (start + end) / 2))
                    else:
                        logging.debug('*Region (%d, %d) is abandoned!' %(start, i))
                    start = i
                    end = i
                    continue
            
            if end - start + 1 >= durationThreshold:
                f.write('%d %05d\n' %(total, (start + end) / 2))
                total += 1
                logging.debug('#Last frame %d is met!' %(end))
                logging.debug('*Region (%d, %d) is valid, and frame %d is selected.' %(start, end, (start + end) / 2))
            
            logging.debug('\nNumber of valid images: %d' %(total))

    elif MODE == 2:
        logging.debug('MODE 2')

        # Read data(fixation point and validation info)
        data = np.genfromtxt(videoDir + '%d.txt' %(videoID), usecols=(2, 3, 6))

        # Hyper-parameters
        dispersionThreshold = 20
        durationThreshold = 8

        # Flag variables
        total = 0
        # This varibale keeps the end frame of the previous region so that we would not
        # generate more than one region that ends at a specific point 
        lastEnd = 0
        # This varibale keeps the frame selected last time so that we would not
        # generate continuous frames
        # However, there are still some frames that are very close to each other
        lastFrame = 0

        # Ref: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.68.2459&rep=rep1&type=pdf
        # Dispersion-Threshold Identification (I-DT)
        with open(listDir + '%d.txt' %(videoID), 'w') as f:
            i = 0
            #while i < 5:
            while i < len(data):
                xmin = config.videoWidth
                xmax = 0
                ymin = config.videoHeight
                ymax = 0
                minThresholdMet = 1

                for j in range(durationThreshold):
                    if i + j >= len(data):
                        break
                    
                    curData = data[i + j]
                    # If the current fixation is invalid, i.e.,
                    # corneal reflection is not detected or fixation point is not in the frame
                    if curData[2] == -1000 or\
                    curData[0] > config.videoWidth or curData[0] < 0 or\
                    curData[1] > config.videoHeight or curData[1] < 0:
                    
                        logging.debug('#Frame %d is invalid' %(i + j))
                        logging.debug('*Region (%d, %d) is abandoned!' %(i, i + j))
                        minThresholdMet = 0
                        # Since this frame is invalid, all the following region must stop here,
                        # so we just set the starting point to the next frame
                        i = i + j
                        break
                    
                    xmin = min(xmin, curData[0])
                    xmax = max(xmax, curData[0])
                    ymin = min(ymin, curData[1])
                    ymax = max(ymax, curData[1])

                    # print i, j, xmin, xmax, ymin, ymax, xmax - xmin + ymax - ymin

                    dispersion = xmax - xmin + ymax - ymin
                    if dispersion > dispersionThreshold:
                        logging.debug('#Dispersion is above the threshold at frame %d' %(i + j))
                        logging.debug('*Region (%d, %d) is abandoned!' %(i, i + j))
                        minThresholdMet = 0
                        break

                j += 1
                while minThresholdMet == 1 and i + j < len(data):
                    curData = data[i + j]
                    middleFrame = (2 * i + j - 1) / 2
                    if curData[2] == -1000 or\
                    curData[0] > config.videoWidth or curData[0] < 0 or\
                    curData[1] > config.videoHeight or curData[1] < 0:
                        f.write('%d %05d\n' %(total, middleFrame))
                        logging.debug('#Frame %d is invalid' %(i + j))
                        logging.debug('*Region (%d, %d) is valid, and frame %d is selected.' %(i, i + j - 1, middleFrame))
                        total += 1
                        i = i + j
                        minThresholdMet = 0
                    
                    xmin = min(xmin, curData[0])
                    xmax = max(xmax, curData[0])
                    ymin = min(ymin, curData[1])
                    ymax = max(ymax, curData[1])

                    # print i, i + j, xmin, xmax, ymin, ymax, xmax - xmin + ymax - ymin

                    dispersion = xmax - xmin + ymax - ymin
                    if dispersion > dispersionThreshold:
                        logging.debug('#Dispersion is above the threshold at frame %d' %(i + j))
                        if i + j == lastEnd:
                            logging.debug('*Region (%d, %d) ends at %d again, and it is abandoned.' %(i, i + j, lastEnd))
                            i = i + j - 1
                        elif middleFrame == lastFrame + 1:
                            logging.debug('*The middle of region (%d, %d) is %d that is close to the previous frame selected, and it is abandoned.' %(i, i + j, middleFrame))
                            pass
                        else:
                            logging.debug('*Region (%d, %d) is valid, and frame %d is selected.' %(i, i + j - 1, middleFrame))
                            f.write('%d %05d\n' %(total, middleFrame))
                            total += 1
                        
                        lastEnd = i + j
                        lastFrame = middleFrame
                        minThresholdMet = 0

                    j += 1

                if minThresholdMet == 1 and j == len(data):
                    middleFrame = (2 * i + j - 1) / 2
                    f.write('%d %05d\n' %(total, middleFrame))
                    logging.debug('#Last frame %d is met!' %(j - 1))
                    logging.debug('*Region (%d, %d) is valid, and frame %d is selected.' %(i, i + j - 1, middleFrame))
                    total += 1
                    break
                
                i += 1

            logging.debug('\nNumber of valid images: %d' %(total))

    elif MODE == 3:
        logging.debug('MODE 3')

        # Read data(fixation point and validation info)
        data = np.genfromtxt(videoDir + '%d.txt' %(videoID), usecols=(2, 3, 6))
        
        # Hyper-parameters
        dispersionThreshold = 20
        durationThreshold = 10

        # Flag variables
        total = 0

        # Modified Dispersion-Threshold Identification (I-DT)
        with open(listDir + '%d.txt' %(videoID), 'w') as f:
            i = 0
            #while i < 5:
            while i < len(data):
                xmin = config.videoWidth
                xmax = 0
                ymin = config.videoHeight
                ymax = 0
                minThresholdMet = 1

                for j in range(durationThreshold):
                    if i + j >= len(data):
                        break
                    
                    curData = data[i + j]
                    # If the current fixation is invalid, i.e.,
                    # corneal reflection is not detected or fixation point is not in the frame
                    if curData[2] == -1000 or\
                    curData[0] > config.videoWidth or curData[0] < 0 or\
                    curData[1] > config.videoHeight or curData[1] < 0:
                    
                        logging.debug('#Frame %d is invalid' %(i + j))
                        logging.debug('*Region (%d, %d) is abandoned!' %(i, i + j))
                        minThresholdMet = 0
                        # Since this frame is invalid, all the following region must stop here,
                        # so we just set the starting point to the next frame
                        i = i + j
                        break
                    
                    xmin = min(xmin, curData[0])
                    xmax = max(xmax, curData[0])
                    ymin = min(ymin, curData[1])
                    ymax = max(ymax, curData[1])

                    # print i, j, xmin, xmax, ymin, ymax, xmax - xmin + ymax - ymin

                    dispersion = xmax - xmin + ymax - ymin
                    if dispersion > dispersionThreshold:
                        logging.debug('#Dispersion is above the threshold at frame %d' %(i + j))
                        logging.debug('*Region (%d, %d) is abandoned!' %(i, i + j))
                        minThresholdMet = 0
                        break

                j += 1
                while minThresholdMet == 1 and i + j < len(data):
                    curData = data[i + j]
                    middleFrame = (2 * i + j - 1) / 2
                    if curData[2] == -1000 or\
                    curData[0] > config.videoWidth or curData[0] < 0 or\
                    curData[1] > config.videoHeight or curData[1] < 0:
                        f.write('%d %05d\n' %(total, middleFrame))
                        logging.debug('#Frame %d is invalid' %(i + j))
                        logging.debug('*Region (%d, %d) is valid, and frame %d is selected.' %(i, i + j - 1, middleFrame))
                        total += 1
                        i = i + j
                        minThresholdMet = 0
                        continue
                    
                    xmin = min(xmin, curData[0])
                    xmax = max(xmax, curData[0])
                    ymin = min(ymin, curData[1])
                    ymax = max(ymax, curData[1])

                    # print i, i + j, xmin, xmax, ymin, ymax, xmax - xmin + ymax - ymin

                    dispersion = xmax - xmin + ymax - ymin
                    if dispersion > dispersionThreshold:
                        logging.debug('#Dispersion is above the threshold at frame %d' %(i + j))
                        logging.debug('*Region (%d, %d) is valid, and frame %d is selected.' %(i, i + j - 1, middleFrame))
                        f.write('%d %05d\n' %(total, middleFrame))
                        total += 1
                        i = i + j - 1
                        minThresholdMet = 0
                        continue

                    j += 1

                if minThresholdMet == 1 and j == len(data):
                    middleFrame = (2 * i + j - 1) / 2
                    f.write('%d %05d\n' %(total, middleFrame))
                    logging.debug('#Last frame %d is met!' %(j - 1))
                    logging.debug('*Region (%d, %d) is valid, and frame %d is selected.' %(i, i + j - 1, middleFrame))
                    total += 1
                    break
                
                i += 1

            logging.debug('\nNumber of valid images: %d' %(total))


if __name__ == "__main__":
    TRAINING = 0
    if sys.argv[1] == 'training':
        TRAINING = 1
        numberOfVideos = config.numberOfTrainingVideo
    elif sys.argv[1] == 'test':
        TRAINING = 0
        numberOfVideos = config.numberOfTestVideo

    if config.DEBUG:
        filterFrame(0, TRAINING)
    else:
        print '#Filter %s frame' %(sys.argv[1])
        for i in range(numberOfVideos):
            print ' *Processing video %d' %(i)
            filterFrame(i, TRAINING)
