import brainflow

from brainflow import BoardIds
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


def main():
    # or BoardIds.NOTION_2_BOARD.value or BoardIds.NOTION_1_BOARD.value
    # print(BoardIds.NOTION_1_BOARD)

    board_id = BoardIds.CROWN_BOARD
    params = BrainFlowInputParams()
    params.board_id = board_id
    BoardShim.enable_dev_board_logger()
    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    print(data)


if __name__ == "__main__":
    main()
