#!/bin/bash
set -e

VIDEONAME=ADOS_0
NUMBEROFVIDEOS=15

IMAGEPATH=data/image/$VIDEONAME/training

LABELING=src/labeling
PRETRAINING=src/preTraining

# Step0
rm -rf $IMAGEPATH/allTrain
rm -rf $IMAGEPATH/allVal
rm -rf $IMAGEPATH/mean
mkdir $IMAGEPATH/allTrain
mkdir $IMAGEPATH/allVal
mkdir $IMAGEPATH/mean

for (( v=0; v<$NUMBEROFVIDEOS; v++ ))
do
    rm -rf $IMAGEPATH/"$v"_crop
    rm -rf $IMAGEPATH/"$v"_train
    rm -rf $IMAGEPATH/"$v"_val

    mkdir $IMAGEPATH/"$v"_crop
    mkdir $IMAGEPATH/"$v"_train
    mkdir $IMAGEPATH/"$v"_val
done

# Step1: Extract frames from the videos
python $PRETRAINING/extractWithoutFixation.py

# Step2: Parse the labeling information
python $LABELING/parse.py training

# Step3: Split the images into training and validation set
python $PRETRAINING/splitImage.py

# Step4: Augment the training set
python $PRETRAINING/augment.py

# Step5: Combine all the training set from different video clips
./$PRETRAINING/combine.sh 1

# Optional: Count the number of images in each category
python $PRETRAINING/count.py

# Step6.1: Create LMDB for training
./$PRETRAINING/createLMDB.sh

# Step6.2: Convert mean file to .npy file
python $PRETRAINING/convert.py $IMAGEPATH/mean/mean.binaryproto $IMAGEPATH/mean/mean.npy

# Step7: Train the network