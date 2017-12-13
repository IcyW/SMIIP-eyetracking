#!/usr/bin/env sh
set -e

TOOLS=./caffe/build/tools

# There are three different modes: 0. Train from scratch; 1. Fine tune; 2. Continue previous training

if [ "$1" -eq 0 ]; then
    $TOOLS/caffe train \
        --solver=caffe/examples/eye_tracking/Alexnet/solver.prototxt 2>&1 | tee -i caffe/examples/eye_tracking/Alexnet/alex_train.log
elif [ "$1" -eq 1 ]; then
    $TOOLS/caffe train \
        --solver=caffe/examples/eye_tracking/Alexnet/solver.prototxt \
        --weights=caffe/models/bvlc_alexnet/bvlc_alexnet.caffemodel 2>&1 | tee -i caffe/examples/eye_tracking/Alexnet/alex_train.log
else
    $TOOLS/caffe train \
    --solver=caffe/examples/eye_tracking/Alexnet/solver.prototxt \
    --snapshot=caffe/examples/eye_tracking/Alexnet/alexnet_train_iter_100.solverstate | tee -i caffe/examples/eye_tracking/Alexnet/alex_train.log
fi
