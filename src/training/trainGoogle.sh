#!/usr/bin/env sh
set -e

TOOLS=./caffe/build/tools

# There are three different modes: 0. Train from scratch; 1. Fine tune; 2. Continue previous training

if [ "$1" -eq 0 ]; then
    $TOOLS/caffe train \
        --solver=caffe/examples/eye_tracking/Googlenet/solver.prototxt 2>&1 | tee -i caffe/examples/eye_tracking/Googlenet/google_train.log
elif [ "$1" -eq 1 ]; then
    $TOOLS/caffe train \
        --solver=caffe/examples/eye_tracking/Googlenet/solver.prototxt \
        --weights=caffe/models/bvlc_googlenet/bvlc_googlenet.caffemodel 2>&1 | tee -i caffe/examples/eye_tracking/Googlenet/google_train.log
else
    $TOOLS/caffe train \
    --solver=caffe/examples/eye_tracking/Googlenet/solver.prototxt \
    --snapshot=caffe/examples/eye_tracking/Googlenet/googlenet_train_iter_100.solverstate | tee -i caffe/examples/eye_tracking/Googlenet/google_train.log
fi
