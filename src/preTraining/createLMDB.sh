#!/usr/bin/env sh
# Create the net lmdb inputs
# N.B. set the path to the imagenet train + val data dirs
set -e

VIDEONAME=ADOS_0
TOOLS=caffe/build/tools

IMAGEPATH=data/image/$VIDEONAME/training
LISTPATH=data/imageList/$VIDEONAME/training

TRAIN_DATA_ROOT=$IMAGEPATH/allTrain/
VAL_DATA_ROOT=$IMAGEPATH/allVal/

rm -rf $IMAGEPATH/train_lmdb
rm -rf $IMAGEPATH/val_lmdb

# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.
RESIZE=true
if $RESIZE; then
  RESIZE_HEIGHT=256
  RESIZE_WIDTH=256
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$TRAIN_DATA_ROOT" ]; then
  echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
  echo "Set the TRAIN_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet training data is stored."
  exit 1
fi

if [ ! -d "$VAL_DATA_ROOT" ]; then
  echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
  echo "Set the VAL_DATA_ROOT variable in create_imacaffeDir = 'caffe/python'
genet.sh to the path" \
       "where the ImageNet validation data is stored."
  exit 1
fi

echo "Creating train lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $TRAIN_DATA_ROOT \
    $LISTPATH/allTrain.txt \
    $IMAGEPATH/train_lmdb

echo "Creating val lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    $VAL_DATA_ROOT \
    $LISTPATH/allVal.txt \
    $IMAGEPATH/val_lmdb

echo "Computing mean..."
# Compute the mean image from the imagenet training lmdb
$TOOLS/compute_image_mean $IMAGEPATH/train_lmdb $IMAGEPATH/mean/mean.binaryproto

echo "Done."
