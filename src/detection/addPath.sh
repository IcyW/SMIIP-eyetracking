#!/bin/bash
set -e

VIDEONAME=$1
NUMBEROFVIDEOS=$2
CUR=$PWD
IMAGEPATH=data/image/$VIDEONAME/test
LISTPATH=data/imageList/$VIDEONAME/test

function addPath {
    awk -v prefix=$CUR/$IMAGEPATH/$1/ '{print prefix $1 ".jpg"}' $LISTPATH/$1.txt > $LISTPATH/$1_full.txt
}

echo "#Add path"
for (( v=0; v<$NUMBEROFVIDEOS; v++ ))
do
    echo "  *Processing video $v"
    addPath $v
done
