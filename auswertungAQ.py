import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import timedelta
from database import writeToArchive
import calendar



AUSWERTUNGSTATISTIKGOING = "data/auswertungStatistikOngoing.csv"
AUSWERTUNGFAHRTENMHD = "data/auswertungFahrtenMHD.csv"
AUSWERTUNGFAHRTENDRK = "data/auswertungFahrtenDRK.csv"
TMPTAGMHD = "data/tmpTagMHD.csv"
TMPTAGDRK = "data/tmpTagDRK.csv"
STATISTIKMHDONGOING = "data/statistikMHDOngoing.csv"
STATISTIKDRKONGOING = "data/statistikDRKOngoing.csv"


mhd = pd.DataFrame({'HiOrg': ['mhd']})
drk = "drk"

def auswertungTag():
    #MHD
    dataMHD = pd.read_csv(AUSWERTUNGFAHRTENMHD)
    datum = dataMHD.at[1, "E-Datum"]
    mhd = "mhd" 
    mhdLable = {'Datum':[datum], 'HiOrg':[mhd]}
    frameLable = pd.DataFrame(data = mhdLable)

    frameMHD = pd.DataFrame(dataMHD, columns = ["Fahrten", "I-Fahrten", "Fernfahrten"])
    mhdTag = frameMHD.sum()
    frameMHDTag = pd.DataFrame(mhdTag)
    frameMHDTag = frameMHDTag.T

    frameMHDTag = frameLable.join(frameMHDTag)

    frameMHDTag.to_csv(TMPTAGMHD)
    

    #DRK
    dataDRK = pd.read_csv(AUSWERTUNGFAHRTENDRK)
    datum = dataDRK.at[1, "E-Datum"]
    drk = "drk" 
    drkLable = {'Datum':[datum], 'HiOrg':[drk]}
    frameLable = pd.DataFrame(data = drkLable)

    frameDRK = pd.DataFrame(dataDRK, columns = ["Fahrten", "I-Fahrten", "Fernfahrten"])
    drkTag = frameDRK.sum()
    frameDRKTag = pd.DataFrame(drkTag)
    frameDRKTag = frameDRKTag.T
    frameDRKTag = frameLable.join(frameDRKTag)
    
    frameDRKTag.to_csv(TMPTAGDRK)
    writeToArchive(TMPTAGMHD, STATISTIKMHDONGOING)
    writeToArchive(TMPTAGDRK, STATISTIKDRKONGOING)

auswertungTag()