#!/bin/bash
set -e

DEBUG=0
AUG=$1
if [ $DEBUG -eq 1 ]
then
    NUMBEROFVIDEOS=2
else
    NUMBEROFVIDEOS=15
fi

VIDEONAME=ADOS_0
IMAGEPATH=data/image/$VIDEONAME/training
LISTPATH=data/imageList/$VIDEONAME/training

# Concatenate all image lists
if [ $AUG -eq 1 ]
then
    cat $LISTPATH/*_trainAug.txt > $LISTPATH/allTrain.txt
else
    awk '{print $1 ".jpg " $2}' $LISTPATH/*_train.txt > $LISTPATH/allTrain.txt
fi

# Add .jpg to val file
awk '{print $1 ".jpg " $2}' $LISTPATH/*_val.txt > $LISTPATH/allVal.txt

# Copy all images to allTrainingImage
for (( v=0; v<$NUMBEROFVIDEOS; v++ ))
do
    cp -r $IMAGEPATH/"$v"_train/.  $IMAGEPATH/allTrain
    cp -r $IMAGEPATH/"$v"_val/.  $IMAGEPATH/allVal
done
