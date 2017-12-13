import pandas as pd
import matplotlib.pyplot as plt

def plot():
    train_log = pd.read_csv("caffe/examples/eye_tracking/Alexnet/alex_train.log.train")
    test_log = pd.read_csv("caffe/examples/eye_tracking/Alexnet/alex_train.log.test")
    fig, ax1 = plt.subplots(figsize=(30, 20))
    ax2 = ax1.twinx()
    ax1.plot(train_log["NumIters"], train_log["loss"], alpha=0.4)
    ax1.plot(test_log["NumIters"], test_log["loss"], 'g')

    #ax2.plot(train_log["NumIters"], train_log["accuracy"], 'y')
    ax2.plot(test_log["NumIters"], test_log["accuracy"], 'r')

    ax1.set_xlabel('iteration')
    ax1.set_ylabel('train loss')
    ax2.set_ylabel('test accuracy')
    plt.show()
    fig.savefig("caffe/examples/eye_tracking/Alexnet/figures/3In1.png")


if __name__ == "__main__":
    plot()
