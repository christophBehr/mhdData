import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import timedelta
import calendar
import itertools



AUSWERTUNGSTATISTIKGOING = "data/auswertungStatistikOngoing.csv"
AUSWERTUNGFAHRTENMHD = "data/auswertungFahrtenMHD.csv"
AUSWERTUNGFAHRTENDRK = "data/auswertungFahrtenDRK.csv"

mhd = ["1-KTW-2", "1-KTW-3", "1-KTW-4", "1-KTW-5", "1-KTW-6"]
drk = ["5-KTW-2", "5-KTW-3", "5-KTW-4", "5-KTW-5", "5-KTW-6", "5-KTW-7", "5-KTW-8", "5-KTW-9"]

def auswertungTag():
    #MHD
    dataMHD = pd.read_csv(AUSWERTUNGFAHRTENMHD)
    frameMHD = pd.DataFrame(dataMHD, columns = ["Fahrten", "I-Fahrten", "Fernfahrten"])
    mhdTag = frameMHD.sum()
    frameMHDTag = pd.DataFrame(mhdTag)
    frameMHDTag = frameMHDTag.T
    print(frameMHDTag)

    #DRK
    dataDRK = pd.read_csv(AUSWERTUNGFAHRTENDRK)
    frameDRK = pd.DataFrame(dataDRK, columns = ["Fahrten", "I-Fahrten", "Fernfahrten"])
    drkTag = frameDRK.sum()
    frameDRKTag = pd.DataFrame(drkTag)
    frameDRKTag = frameDRKTag.T
    print(frameDRKTag)

    

auswertungTag()