import collections
import numpy as np


# HTIL
from acquisition import DataAcquisition

# PyQtGraph
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

import atexit
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


class App:
    def __init__(self, title, sensor_port, sensor_name):
        self.boards = {"ganglion": 1}
        self.update_speed_ms = 100  # config
        self.data_size = 1000
        self.yRange = 1000
        self.streamBuffer = collections.deque(maxlen=self.data_size)
        self.window_size = 4  # config
        self.width = 800  # config
        self.height = 600  # config
        self.sensor = DataAcquisition(
            sensor_port,  self.boards[sensor_name])
        self.sensor.startStreaming()
        self.channels = self.sensor.getChannels()
        self.app = QtGui.QApplication([])
        self.main_layout = pg.GraphicsLayoutWidget(
            title=title, size=(self.width, self.height))
        self.plots = {}  # all plots
        self.filters = {}  # filters
        self.viewIDs = []  # IDs of each view
        self.layouts = {}  # layouts
        self.latestData = []
        self.refresh = None
        self.recoredData = []
        self.channelStreams = [collections.deque(
            maxlen=self.data_size) for channel in self.channels]  # set up channel data streams
        print(self.channelStreams)

    ''' Getters '''

    def getAppGui(self):
        return self.app

    def getLayout(self):
        return self.main_layout

    def getLatestData(self):
        return self.latestData
    ''' '''

    ''' Setters '''

    def setRefresh(self, refreshFunction):
        self.refresh = refreshFunction

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

    def close(self):
        for stream in self.streamBuffer:
            stream.clear()

        self.sensor.end()
        print("done")

    def start(self):
        self.main_layout.show()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
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

    def update(self):
        channels = self.sensor.getChannels()
        # data = self.sensor.getRecentData(self.data_size)  # config
        data = self.sensor.getAllData()

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


def refresh(app):
    print("refresh", app.getLatestData())


def main():
    # run ls /dev/cu.* on unix to find port. On windows use...?
    app = App("My App", '/dev/cu.usbmodem1', "ganglion")  # create app
    print(app.streamBuffer)
    # app.setRefresh(refresh)
    plots = app.addLinePlot("line_series1", yMin=-
                            app.yRange, yMax=app.yRange)
    app.start()


if __name__ == "__main__":
    main()
