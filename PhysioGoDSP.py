from scipy.signal import butter, sosfilt


def butter_lowpass(signal, cutoff, sFreq, order=5):
    sos = butter(order, cutoff, 'lowpass', fs=sFreq, output='sos')
    filtered = sosfilt(sos, signal)
    return filtered


def rectify(signal):
    y = [abs(x) for x in signal]
    return y
