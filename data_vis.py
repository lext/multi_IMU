"""
Visualizer of the data acquired from multi_IMU software.

(c) Aleksei Tiulpin, 2016

Center for Machine Vision and Signal Analysis,
University of Oulu, Finland

"""

import numpy as np
import matplotlib.pyplot as plt
import argparse


if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    data = np.loadtxt(args.filename)

    t = data[:, 0]

    print("Length", t.max() - t.min())
    print("Average dt", np.mean(np.diff(t)), np.std(np.diff(t)))

    acc1 = data[:, 1:4]
    gyro1 = data[:, 4:7]


    acc2 = data[:, 7:10]
    gyro2 = data[:, 10:]

    plt.figure()
    plt.title("Acc 1")
    for i in range(3):
	    plt.plot(t, acc1[:, i])


    plt.figure()
    plt.title("Gyro 1")
    for i in range(3):
	    plt.plot(t, gyro1[:, i])


    plt.figure()
    plt.title("Acc 2")
    for i in range(3):
	    plt.plot(t, acc2[:, i])


    plt.figure()
    plt.title("Gyro 2")
    for i in range(3):
	    plt.plot(t, gyro2[:, i])

    plt.show()
