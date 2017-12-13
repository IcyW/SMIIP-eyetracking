#!/bin/bash
set -e


if [ "$1" -eq 0 ]
then 
    python caffe/tools/extra/parse_log.py --verbose caffe/examples/eye_tracking/Alexnet/alex_train.log caffe/examples/eye_tracking/Alexnet/
    python src/training/plot.py
else
    python caffe/tools/extra/plot_training_log.py 0 caffe/examples/eye_tracking/Alexnet/figures/acc_iters.png caffe/examples/eye_tracking/Alexnet/alex_train.log

    python caffe/tools/extra/plot_training_log.py 1 caffe/examples/eye_tracking/Alexnet/figures/acc_secs.png caffe/examples/eye_tracking/Alexnet/alex_train.log

    python caffe/tools/extra/plot_training_log.py 2 caffe/examples/eye_tracking/Alexnet/figures/testLoss_iters.png caffe/examples/eye_tracking/Alexnet/alex_train.log

    python caffe/tools/extra/plot_training_log.py 3 caffe/examples/eye_tracking/Alexnet/figures/testLoss_secs.png caffe/examples/eye_tracking/Alexnet/alex_train.log

    python caffe/tools/extra/plot_training_log.py 4 caffe/examples/eye_tracking/Alexnet/figures/lr_iters.png caffe/examples/eye_tracking/Alexnet/alex_train.log

    python caffe/tools/extra/plot_training_log.py 5 caffe/examples/eye_tracking/Alexnet/figures/lr_secs.png caffe/examples/eye_tracking/Alexnet/alex_train.log

    python caffe/tools/extra/plot_training_log.py 6 caffe/examples/eye_tracking/Alexnet/figures/trainLoss_iters.png caffe/examples/eye_tracking/Alexnet/alex_train.log

    python caffe/tools/extra/plot_training_log.py 7 caffe/examples/eye_tracking/Alexnet/figures/trainLoss_secs.png caffe/examples/eye_tracking/Alexnet/alex_train.log
fi
