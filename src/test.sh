#!/bin/bash
set -e

VIDEONAME=ADOS_0
NUMBEROFVIDEOS=9

CUR=$PWD
DETECTION=src/detection
PREDICTION=src/prediction
TOOLS=src/tools
IMAGEPATH=data/image/$VIDEONAME/test

# Step0
rm -rf $IMAGEPATH
mkdir $IMAGEPATH

for (( v=0; v<$NUMBEROFVIDEOS; v++ ))
do
    mkdir $IMAGEPATH/$v
    mkdir $IMAGEPATH/"$v"_detection
    mkdir $IMAGEPATH/"$v"_crop
    mkdir $IMAGEPATH/"$v"_prediction
done

PREDONE=1
if [ PREDONE -eq 0 ]
then
# Step1: Filter valid frames from the videos
python $TOOLS/filterFrame.py test

# Step2: Extract the frames
python $TOOLS/readFromVideo.py test

# Step3: Add full path to the image list for detection
./$DETECTION/addPath.sh ADOS_0 $NUMBEROFVIDEOS

# Step4: Detect objects in the images
./$DETECTION/detectYOLO.sh ADOS_0 $NUMBEROFVIDEOS

# Step5: Crop the object-of-interest
python $DETECTION/cropBoundingBox.py

# Optional: Draw the fixation point for better visualization
python $DETECTION/drawCrop.py

# Step6: Parse the labeling information
python $LABELING/parse.py test
fi

# Step7: Predict the cropped images
python $PREDICTION/predict.py

# Step8: Calculate IoU and draw the predictions on the images
python $PREDICTION/calculateIoUAndDraw.py

# Step9: Recreate the videos
# python $PREDICTION/writeToVideo.py