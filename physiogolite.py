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
from brainflow.data_filter import DataFilter
from physiodatastream import Streams


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
        self.initTime = datetime.now().strftime("%H_%M_%S")
        self.board = self.sensor.getBoard()
        self.streams = Streams(self.channels, buffer_size)
        self.main_layout = None
        self.linePlots = []
        self.filterPipeline = None

    def getApp(self):
        return self.app

    def getBoard(self):
        return self.board

    def getStreams(self):
        return self.streams.getStreams()

    def getChannelCount(self):
        return len(self.channels)

    def setFilterPipeline(self, filterFunction):
        self.filterPipeline = filterFunction

    def addLinePlots(self, plots):
        self.linePlots.append(plots)

    def close(self):
        self.sensor.end()
        print("closing")

    def initGUI(self, title, width, height):
        self.main_layout = pg.GraphicsLayoutWidget(
            title=title, size=(width, height))
        self.main_layout.show()
        return self.main_layout

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

    def updateLinePlots(self, data):
        self.streams.update(data)
        for plot in self.linePlots:
            streams = self.getStreams()
            for i, stream in enumerate(streams):
                array = np.array(stream, np.float64)
                # Filter Data
                if (self.filterPipeline != None):
                    array = self.filterPipeline(array)
                plot[i].setData(array)

    def update(self):
        #channels = self.sensor.getChannels()
        t = datetime.now().strftime("%H:%M:%S")
        data = self.sensor.getAllData()
        # Write Data
        if (self.writeData):
            DataFilter.write_file(
                data, f'data/{self.title}_{self.initTime}.csv', 'a')

        self.refresh(data)
        self.updateLinePlots(data)
