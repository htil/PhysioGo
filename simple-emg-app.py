from physiogo import PhysioGo
import numpy as np

from realtime.ioserver import IOServer
import random
from threading import Thread

def refresh(app):
    window_size = 2.0
    channels = [0]
    bands = app.getRecentAvgBandPowers(window_size, channels)
    app.socket.send('data', bands[0].tolist())
    if bands != None:
        label = app.model.predict([bands[0]])
        print("SENDING OVER: ")
        print(label)
        app.socket.send('prediction', label[0]);


def main():
    app = PhysioGo("EMG_Test", '/dev/cu.usbmodem11', "ganglion")  # create app
    plots = app.addLinePlot("line_series1", yMin=-app.yRange, yMax=app.yRange)
    app.loadModel("models/lda-emg-squeeze.pkl")
    socketServer  = IOServer()
    app.setSocketServer(socketServer)
    app.setRefresh(refresh)
    app.setGUIVisibility(False)
    socketServer.runDaemon()
    app.start()


if __name__ == "__main__":
    main()
