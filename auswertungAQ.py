import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import timedelta


BELEGARCHIVONGOING = "data/belegArchivOngoing"

def readData():
    data = pd.read_csv(BELEGARCHIVONGOING, sep = ";", names=["E-Datum", "Einsatz Nr.", "KFZ", "Transport von",
                                                  "Transport nach", "Fahrgast", "Start", "Ende",
                                                  "Infektion", "Tarifzone Num.", "Belegart", "Tarifzone"])
    data = data.iloc[1:]
    auswertungMonat = pd.DataFrame(data) 