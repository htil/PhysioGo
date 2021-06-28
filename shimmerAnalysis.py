from PhysioAnalyze import Study
from PhysioVisualize import plotBasic, plotMulti
from PhysioGoDSP import butter_lowpass, rectify, extractWindows, getMovingAverage, getRMSEnvelope
import numpy as np

# Create Physio Study
sFreq = 512

study = Study(1, "emg", sFreq)

# Read raw csv file

study.readFileOriginal("data/SampleEMG.csv", "\t", 2)
