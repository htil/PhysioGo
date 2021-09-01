import collections
import numpy as np
from datetime import datetime
from threading import Timer
from random import randrange
import pandas as pd
import mne
import matplotlib.pyplot as plt
import joblib


# HTIL
from acquisition import DataAcquisition

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

import atexit
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


class PhysioGo:
    def __init__(self, title, sensor_port, sensor_name, write_data=False, buffer_size=1000):
        self.boards = {"ganglion": 1}
        self.update_speed_ms = 100  # config
        self.data_size = buffer_size
        self.yRange = 1000
        self.window_size = 4  # config
        self.width = 800  # config
        self.height = 600  # config
        self.sensor = DataAcquisition(
            sensor_port,  self.boards[sensor_name])
        self.sensor.startStreaming()
        self.channels = self.sensor.getChannels()
        self.sfreq = self.sensor.getSamplingRate()
        self.app = QtGui.QApplication([])
        self.title = title
        self.main_layout = pg.GraphicsLayoutWidget(
            title=title, size=(self.width, self.height))
        self.plots = {}  # all plots
        self.filters = {}  # filters
        self.viewIDs = []  # IDs of each view
        self.layouts = {}  # layouts
        self.latestData = []
        self.model = None
        self.refresh = None
        self.socket = None
        self.myText = None
        self.writeData = write_data
        self.recoredData = []
        self.date = datetime.now().strftime("%H_%M_%S")
        self.channelStreams = [collections.deque(
            maxlen=self.data_size) for channel in self.channels]  # set up channel data streams
        self.board = self.sensor.getBoard()
        self.visibility = True

    ''' Getters '''

    def getAppGui(self):
        return self.app

    def getBufferSize(self):
        return self.data_size

    def getMainLayout(self):
        return self.main_layout

    def getLatestData(self):
        return self.latestData

    def getRecentAvgBandPowers(self, window_size, channels):
        sensor_data = list(self.getDataStreams())
        stop = self.getBufferSize()
        start = int(stop - (window_size * self.sfreq))
        sensor_data = np.array(sensor_data)
        if (sensor_data.shape[1] >= stop):
            data_in_window = sensor_data[:, start:stop]
            data_in_window = np.array([x for x in data_in_window])
            bands = DataFilter.get_avg_band_powers(
                data_in_window, channels, self.sensor.samplingRate, True)
            return bands

    ''' '''

    ''' Setters '''

    def setRefresh(self, refreshFunction):
        self.refresh = refreshFunction

    def setSocketServer(self, socket):
        self.socket = socket

    def setGUIVisibility(self, visibility):
        self.visibility = visibility

    ''' '''

    def addLinePlot(self, id, row=None, col=None, yMin=-20, yMax=20):
        self.curves = list()
        plots = list()
        self.viewIDs.append(id)
        self.layouts[id] = self.main_layout.addLayout(row=row, col=col)

        # self.layouts[id].addLabel(id)

        # create widget
        for i in range(len(self.channels)):
            p = self.layouts[id].addPlot(row=i, col=0)  # add to widget
            self.plots[id + "_channel_" + str(i)] = p.plot(pen='#A54E4E')
            plots.append(p)
            p.setYRange(yMin, yMax)
        return plots

    def addBasicText(self):
        myViewBox = self.main_layout.addViewBox(border='#A54E4E')
        myViewBox.autoRange()
        self.myText = pg.TextItem("")
        self.myText.setPos(.5, .5)
        myViewBox.addItem(self.myText)

    def close(self):
        for num, stream in enumerate(self.channelStreams):
            print(f'closing stream... {num}')
            stream.clear()

        self.sensor.end()
        print("done")

    def getDataStreams(self):
        return self.channelStreams

    def start(self):
        self.main_layout.show()

        # Main Timer
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)

        # Instruction Timer
        # Maybe move this out also?
        timer2 = QtCore.QTimer()
        timer2.timeout.connect(self.updateInstructions)
        timer2.start(5000)

        ####
        
        QtGui.QApplication.instance().exec_()
        atexit.register(self.close)

    def filter(self, data):

        DataFilter.perform_bandpass(data, self.sensor.samplingRate, 50, 40.0, 1,
                                    FilterTypes.BUTTERWORTH.value, 0)

        '''
        DataFilter.perform_lowpass(data, self.sensor.samplingRate, 100.0, 1,
                                   FilterTypes.BUTTERWORTH.value, 1)
        '''

        return data

    def loadModel(self, fileName):
        self.model = joblib.load(fileName)

    def updateInstructions(self):
        # [100, 99, 98] markers
        classes = ['Rest', 'Lift', 'Squeeze']
        index = randrange(len(classes))
        instruction = classes[index]
        mark = int(100 - index)
        self.board.insert_marker(mark)
        self.myText.setText(instruction)

    def update(self):
        channels = self.sensor.getChannels()
        t = datetime.now().strftime("%H:%M:%S")

        # data = self.sensor.getRecentData(self.data_size)  # config
        # self.board.insert_marker(1)
        data = self.sensor.getAllData()

        if (self.writeData):
            DataFilter.write_file(
                data, f'data/{self.title}_{self.date}.csv', 'a')

        # Update all views

        for count, view_id in enumerate(self.viewIDs):
            for channel_count, channel_id in enumerate(channels):
                for instance in data[channel_id]:
                    self.channelStreams[channel_count].append(instance)
                    array = np.array(
                        self.channelStreams[channel_count], np.float64)
                    processedData = self.filter(array)
                    self.plots[view_id + "_channel_" +
                               str(channel_count)].setData(processedData)

        if (self.refresh != None):
            self.refresh(self)

        self.app.processEvents()
