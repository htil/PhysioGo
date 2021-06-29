from physiogolite import PhysioGo


def update(data):
    print(data)


def main():
    app = PhysioGo("EMG_Test2", '/dev/cu.usbmodem1',
                   "ganglion", write_data=True)
    app.start(update)


main()
