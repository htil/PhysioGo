#import collections
import numpy as np
#from datetime import datetime
#from threading import Timer
#from random import randrange
#import pandas as pd
#import mne
#import matplotlib.pyplot as plt
from physiogo import PhysioGo


# HTIL
#from acquisition import DataAcquisition

# PyQtGraph
#import pyqtgraph as pg
#from pyqtgraph.Qt import QtGui, QtCore

#import atexit
#from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


def main():
    # run ls /dev/cu.* on unix to find port. On windows use...?

    app = PhysioGo("Bryan_EMG_Test", '/dev/cu.usbmodem1',
                   "ganglion", write_data=True)  # create app
    app.addBasicText()
    plots = app.addLinePlot("line_series1", yMin=-app.yRange, yMax=app.yRange)
    app.start()


if __name__ == "__main__":
    main()
