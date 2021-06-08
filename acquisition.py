import argparse
import time
import numpy as np

# Brain
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


class DataAcquisition:
    def __init__(self, serial_port, board_id):
        print("initializing", serial_port, board_id)
        BoardShim.enable_dev_board_logger()
        parser = argparse.ArgumentParser()
        parser.add_argument('--serial-port', type=str,
                            help='serial port', default=serial_port)
        parser.add_argument('--streamer-params', type=str,
                            help='other info', required=False, default='')
        parser.add_argument('--board-id', type=int,
                            help='board id, check docs to get a list of supported boards', default=board_id)
        self.args = parser.parse_args()
        #self.window_size = window_size

        params = BrainFlowInputParams()
        params.serial_port = self.args.serial_port
        self.board = BoardShim(self.args.board_id, params)
        self.board.prepare_session()
        self.board.config_board('n')
        self.channels = BoardShim.get_exg_channels(board_id)
        self.samplingRate = BoardShim.get_sampling_rate(board_id)
        self.markerChannel = BoardShim.get_marker_channel(board_id)
        info = BoardShim.get_accel_channels(board_id)
        print("info: ", info)

    def getAllData(self):
        # get all data and remove it from internal buffer
        return self.board.get_board_data()

    def getBoard(self):
        return self.board

    def getChannels(self):
        return self.channels

    def getMarkerChannel(self):
        return self.markerChannel

    def getRecentData(self, points):
        # do not remove data from buffer
        return self.board.get_current_board_data(points)

    def getSamplingRate(self):
        return self.samplingRate

    def end(self):
        print("Ending Stream")
        self.board.stop_stream()
        self.board.release_session()

    def startStreaming(self):
        # self.board.start_stream () # use this for default options
        print('Starting Stream')
        self.board.start_stream(45000, self.args.streamer_params)
        time.sleep(1)

        # data = board.get_board_data()  # get all data and remove it from internal buffer
        #data = self.board.get_current_board_data(256)
        # print(data)
