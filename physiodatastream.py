import collections


class Streams:
    def __init__(self, channels, buffer_size):
        self.channelStreams = [collections.deque(
            maxlen=buffer_size) for channel in channels]
        self.channels = channels

    def update(self, data):
        for channelCount, channel in enumerate(self.channels):
            for sample in data[channel]:
                self.channelStreams[channelCount].append(sample)

    def getStreams(self):
        return self.channelStreams
