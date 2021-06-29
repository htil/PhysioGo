from brainflow.data_filter import DataFilter
import pandas as pd
import numpy as np
import mne
import csv


class Study:
    def __init__(self, num_channels, channel_type, fs, eventMapping=None, eventFile=None):
        self.raw = None
        self.currentFile = None
        self.currentFileDf = []
        self.channelTypes = [channel_type] * num_channels
        self.mneFactor = 1000000  # account for unit conversion if necessary
        self.channelNames = [str(n) for n in range(num_channels)]
        self.sfreq = fs

        # Create events
        if eventFile != None:
            self.events = mne.read_events(eventFile)
        else:
            self.events = []

        self.info = mne.create_info(
            ch_names=self.channelNames, sfreq=self.sfreq, ch_types=self.channelTypes)

    def readFile(self, location, firstColumn=0, lastColumn=1):
        self.currentFile = DataFilter.read_file(location)
        #self.currentFileDf = pd.DataFrame(np.transpose(self.currentFile))
        # only accounts for 1 channel currently
        res = self.currentFile[firstColumn:lastColumn] / self.mneFactor
        self.raw = mne.io.RawArray(res, self.info)
        print(f'Read {location}')

    def updateRaw(self, data):
        res = data / 1
        self.raw = mne.io.RawArray(res, self.info)
        print(self.raw)

    def readFileOriginal(self, location, seperator, skiprows):
        array = []
        print(f'Reading {location}')
        with open(location, 'r') as f:
            reader = csv.reader(f,  delimiter=seperator)
            for x, row in enumerate(reader):
                if x > skiprows:
                    array.append(row)
        return np.array(array)

    def getEvents(self):
        return self.events

    # Should return seconds
    def getEventTime(self, eventNum):
        return int(self.events[eventNum][0] / self.sfreq)

    def getEpoch(self, start, eventDuration):
        start = start * self.sfreq
        duration = eventDuration * self.sfreq
        stop = start + duration
        data, times = self.raw.get_data(
            return_times=True, start=start, stop=stop)
        return data, times
