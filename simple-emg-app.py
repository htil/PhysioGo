from physiogo import PhysioGo
import numpy as np


def refresh(app):
    window_size = 2.0
    channels = [0]
    bands = app.getRecentAvgBandPowers(window_size, channels)
    if bands != None:
        label = app.model.predict([bands[0]])
        print(label)


def main():
    app = PhysioGo("EMG_Test", '/dev/cu.usbmodem1', "ganglion")  # create app
    plots = app.addLinePlot("line_series1", yMin=-app.yRange, yMax=app.yRange)
    app.loadModel("models/lda-emg-squeeze.pkl")
    app.setRefresh(refresh)
    app.start()


if __name__ == "__main__":
    main()
