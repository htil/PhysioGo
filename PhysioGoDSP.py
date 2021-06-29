from scipy.signal import butter, sosfilt
import numpy as np


def butter_lowpass(signal, cutoff, sFreq, order=5):
    sos = butter(order, cutoff, 'lowpass', fs=sFreq, output='sos')
    filtered = sosfilt(sos, signal)
    return filtered


def rectify(signal):
    y = [abs(x) for x in signal]
    return y


# windowSize = seconds
# this sliding window implementation is slow. Fix with numpy vectorization.
def extractWindows(signal, windowSize, overlap):
    windowStart = 0
    numOfSamples = len(signal)
    windows = []

    #print(f'numOfSamples {numOfSamples}')
    while windowStart + int(windowSize) < numOfSamples:
        stop = int(windowStart + windowSize)
        window = signal[windowStart:stop]
        windows.append(window)
        windowStart = int(windowStart + windowSize) - overlap
        #print(f'samples: {numOfSamples}, windowStart {windowStart}')
    return np.vstack(windows)


def getMovingAverage(signal, times, windowSize):
    overlap = windowSize - 1
    windows = extractWindows(signal, windowSize, overlap)
    movingAvg = windows.mean(axis=1)
    sampleGap = len(times) - len(movingAvg)
    paddedMovingAvg = np.pad(movingAvg, (sampleGap, 0), 'edge')
    return paddedMovingAvg


def getRMSEnvelope(signal, times, windowSize):
    overlap = windowSize - 1
    windows = extractWindows(signal, windowSize, overlap)
    rmsEnvelope = [getRMS(signalWindow) for signalWindow in windows]
    sampleGap = len(times) - len(rmsEnvelope)
    paddedRMS = np.pad(rmsEnvelope, (sampleGap, 0), 'edge')
    return paddedRMS


def getRMS(signalWindow):
    y = np.array(signalWindow)
    rms = np.sqrt(np.mean(y**2))
    return rms
