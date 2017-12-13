#!/usr/bin/python
from src import config

import numpy as np
import logging
import csv
import PIL
from PIL import Image, ImageDraw, ImageFont


def inBBox(fixation, bbox):
    """
    # Hard boundary
    if fixation[0] >= bbox[0] and fixation[0] <= bbox[2] and fixation[1] >= bbox[1] and fixation[1] <= bbox[3]:
        return True
    else:
        return False
    """

    # Allow a little deviation. TO TUNE
    if fixation[0] >= bbox[0] - config.deviationX and fixation[0] <= bbox[2] + config.deviationX and fixation[1] >= bbox[1] - config.deviationY and fixation[1] <= bbox[3]+ config.deviationY:
        return True
    else:
        return False

def calculateIoU(bbox, bboxGT):
    xmin = max(bbox[0], bboxGT[0])
    ymin = max(bbox[1], bboxGT[1])
    xmax = min(bbox[2], bboxGT[2])
    ymax = min(bbox[3], bboxGT[3])

    intersection = (xmax - xmin + 1) * (ymax - ymin + 1)

    bboxArea = (bbox[2] - bbox[0] + 1) * (bbox[3] - bbox[1] + 1)
    bboxGTArea = (bboxGT[2] - bboxGT[0] + 1) * (bboxGT[3] - bboxGT[1] + 1)

    IoU = intersection / float(bboxArea + bboxGTArea - intersection)

    return IoU

def calculateIoUAndDraw(videoID):
    prediction = np.genfromtxt(config.testListDir + '%d_briefPrediction.txt' %(videoID), dtype=None)
    mapping = np.genfromtxt(config.testListDir + '%d.txt' %(videoID), dtype=int)
    fixation = np.genfromtxt(config.testVideoDir + '%d.txt' %(videoID), usecols=(2, 3))
    bbox = np.genfromtxt(config.testListDir + '%d_crop.txt' %(videoID), dtype=int)

    groundTruth = {}
    with open(config.testListDir + '%d_groundtruth.txt' %(videoID), 'r') as f:
        reader = csv.reader(f)
        for rows in reader:
            data = rows[0].split(' ')
            key = int(data[0])
            if groundTruth.has_key(key):    
                groundTruth[key].append(data[1:])
            else:
                groundTruth[key] = [data[1:],]


    radius = 5
    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeSerifBold', 20)

    correctCount = 0
    for i in range(len(prediction)):
        imgId = prediction[i][0]

        """
        # For DEBUG only
        if config.DEBUG:
            if videoID == 0 and not (imgId == 0 or imgId == 26 or imgId == 36):
                continue
            if videoID == 1 and not (imgId == 0 or imgId == 19):
                continue
        """

        img = Image.open(config.testImageDir + '%d/%d.jpg' %(videoID, imgId))
        draw = ImageDraw.Draw(img)

        logging.debug('Image: %d' %(imgId))

        pos = mapping[imgId][1]
        curFixation = fixation[pos]
        x = curFixation[0]
        y = curFixation[1]
        logging.debug('#Current fixation: %.2f, %.2f' %(x, y))
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(0, 0, 255, 0))
        draw.line((0, y, config.videoWidth, y), fill=(0, 0, 255, 0), width=3)
        draw.line((x, 0, x, config.videoHeight), fill=(0, 0, 255, 0), width=3)


        bboxPredict = bbox[i]
        probPredict = prediction[i][1]
        classPredict = prediction[i][2]
        labelPredict = prediction[i][3]
        logging.debug('#Current predicted bbox: %s %s' %(np.array_str(bboxPredict), labelPredict))
        for delta in range(5):
            xmin = max(0, bboxPredict[1] + delta)
            ymin = max(0, bboxPredict[2] + delta)
            xmax = min(config.videoWidth, bboxPredict[3] - delta)
            ymax = min(config.videoHeight, bboxPredict[4] - delta)
            draw.rectangle([xmin, ymin, xmax, ymax], outline=(0, 255, 255, 0))

        draw.text((0, 0), "Prob: %s, Labels: %s" %(probPredict, labelPredict), font=fnt, fill=(0, 0, 0, 255))

        gtAll = groundTruth[imgId]
        flag = 0
        gtPartial = []
        for gt in gtAll:
            bboxGT = [int(coor) for coor in gt[:4]]
            if inBBox(curFixation, bboxGT):
                gtPartial.append(gt)

        if len(gtPartial) > 1:
            gt = gtPartial[0]
            for i in range(1, len(gtPartial)):
                center = [(int(gtPartial[i][0]) + int(gtPartial[i][2])) / 2, (int(gtPartial[i][1]) + int(gtPartial[i][3])) / 2]
                gtCenter = [(int(gt[0]) + int(gt[2])) / 2, (int(gt[1]) + int(gt[3])) / 2]
                curDist = np.linalg.norm(center - curFixation)
                gtDist = np.linalg.norm(gtCenter - curFixation)
                if curDist < gtDist:
                    gt = gtPartial[i]
        elif len(gtPartial) == 1:
            gt = gtPartial[0]
        else:
            if classPredict != config.labels_to_ind['Other']:
                logging.debug('    @Wrongly predicted Other as %s' %(labelPredict))
                draw.text((0, 20), 'Wrongly predicted Other as %s' %(labelPredict), font=fnt, fill=(0, 0, 0, 255))
            else:
                logging.debug('    @Correctly predicted Other')
                draw.text((0, 20), 'Correctly predicted Other', font=fnt, fill=(0, 0, 0, 255))
                correctCount += 1
            final.write('%d_%d %d %d 0\n' %(videoID, imgId, classPredict, config.labels_to_ind['Other']))
            gt = None

        if gt != None:
            bboxGT = [int(coor) for coor in gt[:4]]
            classGT = int(gt[4])
            labelGT = gt[5]

            logging.debug('    *Current ground truth bbox: %s %s' %(' '.join(map(str, bboxGT)), labelGT))

            IoU = calculateIoU(bboxPredict[1:], bboxGT)
            if classPredict != classGT:
                logging.debug('    @Wrongly predicted %s as %s with IoU %f' %(labelGT, labelPredict, IoU))
                draw.text((0, 20), 'Wrongly predicted %s as %s with IoU %f' %(labelGT, labelPredict, IoU), font=fnt, fill=(0, 0, 0, 255))
            else:
                logging.debug('    @Correctly predicted %s with IoU %f' %(labelPredict, IoU))
                draw.text((0, 20), 'Correctly predicted %s with IoU %f' %(labelPredict, IoU), font=fnt, fill=(0, 0, 0, 255))
                correctCount += 1
            final.write('%d_%d %d %d %f\n' %(videoID, imgId, classPredict, classGT, IoU))

            for delta in range(5):
                xmin = max(0, bboxGT[0] + delta)
                ymin = max(0, bboxGT[1] + delta)
                xmax = min(config.videoWidth, bboxGT[2] - delta)
                ymax = min(config.videoHeight, bboxGT[3] - delta)

                draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0, 0))

        """
        for delta in range(5):
            xmin = max(0, bboxGT[0] + delta)
            ymin = max(0, bboxGT[1] + delta)
            xmax = min(config.videoWidth, bboxGT[2] - delta)
            ymax = min(config.videoHeight, bboxGT[3] - delta)

            draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 255, 0, 0))
        """
        #print videoID, imgId
        img.save(config.testImageDir + '%d_prediction/%d.jpg' %(videoID, imgId))

    print 'Correctly predict %d images out of %d.\n' %(correctCount, len(prediction))


if __name__ == "__main__":
    if config.DEBUG:
        calculateIoUAndDraw(0)
        calculateIoUAndDraw(1)
    else:
        final = open(config.testListDir + 'final.txt', 'w')
        print '#Calculate IoU and draw prediction'
        for i in range(config.numberOfTestVideo):
            print ' *Processing video %d' %(i)
            calculateIoUAndDraw(i)
