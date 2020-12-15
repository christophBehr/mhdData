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


mhdKTW = 5
drkKTW = 8
wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]


def auswertungTag():
    
    dataMHD = pd.read_csv(AUSWERTUNGFAHRTENMHD)
    dataDRK = pd.read_csv(AUSWERTUNGFAHRTENDRK)

    datum = dataMHD.at[1, "E-Datum"]
    datumLable = {'Datum':[datum]}
    frameLable = pd.DataFrame(data = datumLable)

    #MHD
    frameMHD = pd.DataFrame(dataMHD, columns = ["Fahrten", "I-Fahrten", "Fernfahrten"])
    frameMHD = frameMHD.rename(columns = {"Fahrten":"Fahrten-MHD", "I-Fahrten":"I-Fahrten-MHD", "Fernfahrten":"Fernfahrten-MHD"})
    mhdTag = frameMHD.sum()
    frameMHDTag = pd.DataFrame(mhdTag)
    frameMHDTag = frameMHDTag.T

    #DRK
    frameDRK = pd.DataFrame(dataDRK, columns = ["Fahrten", "I-Fahrten", "Fernfahrten"])
    frameDRK = frameDRK.rename(columns = {"Fahrten":"Fahrten-DRK", "I-Fahrten":"I-Fahrten-DRK", "Fernfahrten":"Fernfahrten-DRK"})
    drkTag = frameDRK.sum()
    frameDRKTag = pd.DataFrame(drkTag)
    frameDRKTag = frameDRKTag.T

    #Fahrten im Schnitt je KTW MHD
    auslastungMHD = frameMHDTag[["Fahrten-MHD"]]
    proKTWMHD = auslastungMHD.div(mhdKTW)
    proKTWMHD = proKTWMHD.rename(columns={"Fahrten-MHD":"Auslastung-MHD"})
    frameMHDTag = frameMHDTag.join(proKTWMHD)

    #Farhten im Schnitt je KTW DRK
    auslastungDRK = frameDRKTag[["Fahrten-DRK"]]
    proKTWDRK = auslastungDRK.div(drkKTW)
    proKTWDRK = proKTWDRK.rename(columns={"Fahrten-DRK":"Auslastung-DRK"})
    frameDRKTag = frameDRKTag.join(proKTWDRK)

    frameTag = frameMHDTag.join(frameDRKTag)
    frameTag = frameLable.join(frameTag)
    
    frameTag["Fahrten Gesamt"] = frameTag["Fahrten-MHD"] + frameTag["Fahrten-DRK"]
    frameTag["i-Fahrten Gesamt"] = frameTag["I-Fahrten-MHD"] + frameTag["I-Fahrten-DRK"]
    
    frameTag["Datum"] = pd.to_datetime(frameTag.Datum)
    tag = wochentage[int(frameTag.Datum.dt.weekday)]
    frameTag.insert(loc=0, column = "Wochentag", value = tag)

    print(frameTag)
    
    

    
    frameMHDTag.to_csv(TMPTAGMHD)
    frameDRKTag.to_csv(TMPTAGDRK)
    #writeToArchive(TMPTAGMHD, STATISTIKMHDONGOING)
    #writeToArchive(TMPTAGDRK, STATISTIKDRKONGOING)
    return(frameTag)

auswertungTag()