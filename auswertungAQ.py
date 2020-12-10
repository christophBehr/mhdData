import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import timedelta

PATHTXT = "exportArchiv.txt"
BELEGARCHIV = "data/belegArchiv.csv"
KTWFMS = "data/ktwFMS.csv"
FAHRTENSTATISTIK = "data/fahrtenStatistik.csv"
ABRECHNUNG = "data/abrechnung.csv"
AUSWERTUNGFMS = "data/auswertungFMS.csv"
AUSWERTUNGSTATISTIK = "data/auswertungStatistik.csv"

def readData():
    data = pd.read_csv(PATHTXT, sep = ";", names=["E-Datum", "Einsatz Nr.", "KFZ", "Transport von",
                                                  "Transport nach", "Fahrgast", "Start", "Ende",
                                                  "Infektion", "Tarifzone Num.", "Belegart", "Tarifzone"])
    data = data.iloc[1:]
    auswertungMonat = pd.DataFrame(data) 