#!/bin/bash
set -e

THRESHOLD=0.1

NUMBEROFVIDEOS=9
VIDEONAME=$1
CUR=$PWD
DARKNET=darknet
IMAGEPATH=$PWD/data/image/$VIDEONAME/test
LISTPATH=$PWD/data/imageList/$VIDEONAME/test

function detectYOLO {
    cd $DARKNET

    ./darknet detect cfg/yolo.cfg weights/yolo.weights -thresh $THRESHOLD < $LISTPATH/$1_full.txt > $LISTPATH/$1_detection.txt

    cd $CUR
}

echo "#Detect YOLO"
for (( v=0; v<$NUMBEROFVIDEOS; v++ ))
do
    echo "  *Processing video $v"
    detectYOLO $v
done
