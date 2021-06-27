import matplotlib.pyplot as plt


def plotBasic(data, times, size, title=""):
    fig, ax = plt.subplots(figsize=(size[0], size[1]))
    plt.title(title)
    ax.plot(times, data)
    return fig, ax


def plotMulti(data, labels, times, size, xLabel="", yLabel="", title="", legend=True):
    fig, ax = plt.subplots(figsize=(size[0], size[1]))
    for x, signal in enumerate(data):
        ax.plot(times, signal, label=labels[x])
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    plt.title(title)
    if (legend):
        ax.legend()
    return fig, ax
