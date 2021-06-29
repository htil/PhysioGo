import collections
import numpy as np
from datetime import datetime
from threading import Timer
from random import randrange
import pandas as pd
import mne
import matplotlib.pyplot as plt
import joblib
import sys


# HTIL
from acquisition import DataAcquisition

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

import atexit
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


class PhysioGo:
    def __init__(self, title, sensor_port, sensor_name, write_data=False, buffer_size=1000, update_speed=100):
        self.boards = {"ganglion": 1}
        self.sensor = DataAcquisition(
            sensor_port,  self.boards[sensor_name])
        self.sensor.startStreaming()
        self.channels = self.sensor.getChannels()
        self.sfreq = self.sensor.getSamplingRate()
        self.update_speed_ms = update_speed  # config
        self.app = QtGui.QApplication([])
        self.refresh = None
        self.writeData = write_data
        self.title = title
        self.date = datetime.now().strftime("%H_%M_%S")

    def start(self, refresh):
        print("starting... ")
        self.refresh = refresh
        # Main Timer
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        self.refresh = refresh
        QtGui.QApplication.instance().exec_()
        atexit.register(self.close)

    def update(self):
        #channels = self.sensor.getChannels()
        t = datetime.now().strftime("%H:%M:%S")
        data = self.sensor.getAllData()
        self.refresh(data)
        if (self.writeData):
            DataFilter.write_file(
                data, f'data/{self.title}_{self.date}.csv', 'a')

    def close(self):
        self.sensor.end()
        print("closing")
