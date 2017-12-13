#!/usr/bin/python
from src import config

import numpy as np
import itertools
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    Ref: http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        np.round(cm, 2, cm)
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix without normalization')

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def evaluate():
    final = np.genfromtxt(config.testListDir + 'final.txt', usecols=(1,2,3))
    gt = final[:,1]
    prediction = final[:,0]
    correct = gt == prediction
    correctCount = np.count_nonzero(correct)
    confusion = confusion_matrix(gt, prediction)

    IoU = np.multiply(final[:,2], correct)
    print np.sum(IoU) / np.count_nonzero(IoU)

    class_names = config.labels
    # Plot non-normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(confusion, classes=class_names,
                        title='Confusion matrix, without normalization')

    # Plot normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(confusion, classes=class_names, normalize=True,
                        title='Normalized confusion matrix')

    plt.show()

    print 'Correctly predict %d images out of %d.\n' %(correctCount, len(gt)) 

if __name__ == "__main__":
    print '#Evaluate final result'
    evaluate()
