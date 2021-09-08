from physiogolite import PhysioGo
from visualizations import linePlots
import numpy as np
from PhysioGoDSP import getMovingAverage, rectify
import time


class App:
    def __init__(self, appID, port, deviceID):
        self.context = PhysioGo(appID, port,
                                deviceID, write_data=False, update_speed=100)
        self.GUI = self.context.initGUI("Test", 500, 500)
        self.linePlots = linePlots(self.GUI, self.context.getChannelCount())
        self.context.addLinePlots(self.linePlots)
        self.context.setFilterPipeline(self.filter)
        self.startTime = time.time()
        self.context.start(self.update)

    def filter(self, data):
        return getMovingAverage(data, data, int(len(data) * 0.05))

    def update(self, data):
        print(self.startTime)
        pass


App("EMG_Test2", '/dev/cu.usbmodem1', "ganglion")
