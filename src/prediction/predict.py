#!/usr/bin/python
from src import config

import sys
import numpy as np
import caffe

caffe.set_mode_gpu()


def predict(videoID, modelName, FINETUNE, DETECTION):
    model_def = modelDir + 'deploy.prototxt' 
    model_weights = modelDir + modelName

    net = caffe.Net(model_def,      # defines the structure of the model
                    model_weights,  # contains the trained weights
                    caffe.TEST)     # use test mode (e.g., don't perform dropout)

    # load the mean image
    if FINETUNE:
        mu = np.load('caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')
    else:
        mu = np.load(config.trainingImageDir + 'mean/mean.npy')
    mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values

    #print mu

    # create transformer for the input called 'data'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
    transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
    transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

    # set the size of the input (we can skip this if we're happy
    #  with the default; we can also change it later, e.g., for different batch sizes)
    batch_size = 96

    if modelType == 'Alexnet':
        net.blobs['data'].reshape(batch_size, 3, 227, 227)
    else:
        net.blobs['data'].reshape(batch_size, 3, 224, 224)


    imageList = np.genfromtxt(config.testListDir + '%d_crop.txt' %(videoID), dtype='str', usecols=(0))
    numberOfImages = len(imageList)
    #numberOfImages = 200

    blobImage = []
    briefF = open(config.testListDir + '%d_briefPrediction.txt' %(videoID), 'w')
    f =  open(config.testListDir + '%d_prediction.txt' %(videoID), 'w')

    if DETECTION:
        for i in range(numberOfImages):
            image = caffe.io.load_image(config.testImageDir + '%d_crop/%s.jpg' %(videoID, imageList[i]))
            transformed_image = transformer.preprocess('data', image)
            blobImage.append(transformed_image)

            if i % batch_size == batch_size - 1 or i == numberOfImages - 1:
                blobLen = len(blobImage)
                if blobLen < batch_size:
                    for app in range(batch_size - blobLen):
                        if modelType == 'Alexnet':
                            blobImage.append(np.zeros([3, 227, 227]))
                        else:
                            blobImage.append(np.zeros([3, 224, 224]))

                net.blobs['data'].data[...] = blobImage
                output = net.forward()

                output_prob = output['prob']
                #print output_prob

                for j in range(blobLen):
                    top_inds = output_prob[j].argsort()[::-1][:5]
                    imageListIndex = i / batch_size * batch_size + j
                    f.write('%s\n' %(imageList[imageListIndex]))
                    for item in zip(output_prob[j][top_inds], np.array(config.labels)[top_inds]):
                        f.write('%s\n' %(str(item)))
                    f.write('\n')

                    briefF.write('%s %f %d %s\n' %(imageList[imageListIndex], output_prob[j][top_inds[0]], top_inds[0], config.ind_to_labels[top_inds[0]]))
                
                blobImage = []
    else:
        deltaList = [32, 48, 64]
        numberOfDelta = len(deltaList)
        miniBatchSize = batch_size / numberOfDelta
        for i in range(numberOfImages):
            for delta in deltaList:
                image = caffe.io.load_image(config.testImageDir + '%d_crop/%d/%s.jpg' %(videoID, delta, imageList[i]))
                transformed_image = transformer.preprocess('data', image)
                blobImage.append(transformed_image)

            if (i + 1) * numberOfDelta % batch_size == 0 or i == numberOfImages - 1:
                blobLen = len(blobImage)
                if blobLen < batch_size:
                    for app in range(batch_size - blobLen):
                        #blobImage.append(np.zeros([3, 224, 224]))
                        blobImage.append(np.zeros([3, 227, 227]))

                net.blobs['data'].data[...] = blobImage
                output = net.forward()

                output_prob = output['prob']

                for j in range(0, blobLen, numberOfDelta):
                    #print imageList[i / miniBatchSize * miniBatchSize + j / numberOfDelta]

                    whole_prob = 0
                    for k in range(numberOfDelta):
                        whole_prob += output_prob[j + k]
                        top_inds = output_prob[j + k].argsort()[::-1][:5]
                        f.write('%s_%d\n' %(imageList[i / miniBatchSize * miniBatchSize + j / numberOfDelta], deltaList[k]))
                        for item in zip(output_prob[j + k][top_inds], np.array(config.labels)[top_inds]):
                            f.write('%s\n' %(str(item)))

                    top_inds = whole_prob.argsort()[::-1][:5]
                    f.write('%s_combination\n' %(imageList[i / miniBatchSize * miniBatchSize + j / numberOfDelta]))
                    for item in zip(whole_prob[top_inds] / numberOfDelta, np.array(config.labels)[top_inds]):
                        f.write('%s\n' %(str(item)))

                    briefF.write('%s %f %d %s\n' %(imageList[i / miniBatchSize * miniBatchSize + j / numberOfDelta], whole_prob[top_inds[0]] / numberOfDelta, top_inds[0], config.ind_to_labels[top_inds[0]]))

                    f.write('\n')

                blobImage = []


if __name__ == "__main__":
    FINETUNE = 1
    modelType = 'Alexnet'
    modelDir = 'caffe/examples/eye_tracking/' + modelType + '/'

    modelName = 'alexnet_train_iter_1000.caffemodel'
    #modelName = 'googlenet_train_iter_1000.caffemodel'

    if config.DEBUG:
        predict(0, modelName, FINETUNE, config.DETECTION)
        predict(1, modelName, FINETUNE, config.DETECTION)
    else:
        print '#Predict'
        for i in range(config.numberOfTestVideo):
            print ' *Processing video %d' %(i)
            predict(i, modelName, FINETUNE, config.DETECTION)
