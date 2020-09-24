import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta


PATHTXT = "exportArchiv.txt"
BELEGARCHIV = "data/belegArchiv.csv"
KTWFMS = "data/ktwFMS.csv"
FAHRTENSTATISTIK = "data/fahrtenStatistik.csv"
ABRECHNUNG = "data/abrechnung.csv"
AUSWERTUNGFMS = "data/auswertungFMS.csv"
AUSWERTUNGSTATISTIK = "data/auswertungStatistik.csv"
def data():
    """
    Konvertiert den .txt Exportr aus dem Belegarchiv in eine .csv Datei
    """
    global belegArchiv
    data = pd.read_csv(PATHTXT, sep = ";", names=["E-Datum", "Einsatz Nr.", "KFZ", "Transport von",
                                                  "Transport nach", "Fahrgast", "Start", "Ende",
                                                  "Infektion", "Tarifzone Num.", "Belegart", "Tarifzone"])
    data = data.iloc[1:]
    belegArchiv = pd.DataFrame(data)
    belegArchiv.to_csv(BELEGARCHIV, encoding='utf-8')
    return(belegArchiv)


def ktwFMS(belegArchiv):
    """
    Erzeugt die DB für die Zeiterfassung,
    Parmeter: E-Datum, KFZ, Start, Ende,
    """
    global ktwFMS
    ktwFMS = belegArchiv[["E-Datum", "KFZ", "Start", "Ende"]]

    ktwFMS.to_csv(KTWFMS, encoding='utf-8')
    return(ktwFMS)


def fahrtenStatistik(belegArchiv):
    """
    Erzeugt die DB für die Fahrtenstatistik
    Parameter: E-Datum, KFZ, Transport nach, Infektion
    """
    global fahrtenStatistik
    fahrtenStatistik = belegArchiv[["E-Datum", "KFZ", "Transport nach", "Infektion"]]
   
    fahrtenStatistik.to_csv(FAHRTENSTATISTIK, encoding='utf-8')
    return(fahrtenStatistik)

def abrechnung(belegArchiv):
    """
    Erzeugt die DB für die Abrechung,
    Parameter: E-Datum, KFZ, Einsatz NR, Transport von, Transport nach, Fahrgast, Tarifzone Num, Belegart, Tarifzone
    """
    global abrechnung
    abrechnung = belegArchiv[["E-Datum", "Einsatz Nr.", "KFZ", "Transport von", "Transport nach", "Fahrgast", "Tarifzone Num.", "Belegart", "Tarifzone"]]

    abrechnung.to_csv(ABRECHNUNG, encoding='utf-8')
    return(abrechnung)


def strfdelta(timedelta, fmt):
    """
    Format für timedelta Objekte. Es werden nur Stunden und Minuten angezeigt
    """
    d = {'days': timedelta.days}
    d['hours'], rem = divmod(timedelta.seconds, 3600)
    d['minutes'], d['seconds'] = divmod(rem, 60)
    return(fmt.format(**d))


def auswertungFMS(ktwFMS):
    """
    Erzeugt die Auswertungen der Standzeiten aus der ktwFMS DB
    """
    #ausrueck =  aprox Zeit von alarmierung bis abholzeit
    ausrueck = timedelta(days = 0, hours = 0, minutes = 30)

    '''
    Instanziere Dienstzeiten KTW 1-6
    '''
    dienst12 = '06:00'
    start12 = dt.datetime.strptime(dienst12, '%H:%M')
    dienst13 = '06:30'
    start13 = dt.datetime.strptime(dienst13, '%H:%M')
    dienst14 = '07:00'
    start14 = dt.datetime.strptime(dienst14, '%H:%M')
    dienst15 = '08:30'
    start15 = dt.datetime.strptime(dienst15, '%H:%M')
    dienst16 = '09:30'
    start16 = dt.datetime.strptime(dienst16, '%H:%M')
    
    ktwFMS["Start"] = pd.to_datetime(ktwFMS["Start"], format = "'%H:%M'")
    ktwFMS.sort_values(by = ["KFZ", "Start"])

    ktwFMS12 = ktwFMS.loc[ktwFMS["KFZ"] == "'1-KTW-2'"]
    erste12 = ktwFMS12[0:1]
    obj12 = erste12.iloc[0]["Start"]
    delta12 = obj12 - start12 - ausrueck
    
    ktwFMS13 = ktwFMS.loc[ktwFMS["KFZ"] == "'1-KTW-3'"]
    erste13 = ktwFMS13[0:1]
    obj13 = erste13.iloc[0]["Start"]
    delta13 = obj13 - start13 - ausrueck
    
    ktwFMS14 = ktwFMS.loc[ktwFMS["KFZ"] == "'1-KTW-4'"]
    erste14= ktwFMS14[0:1]
    obj14 = erste14.iloc[0]["Start"]
    delta14 = obj14 - start14 - ausrueck
    
    ktwFMS15 = ktwFMS.loc[ktwFMS["KFZ"] == "'1-KTW-5'"]
    erste15 = ktwFMS15[0:1]
    obj15 = erste15.iloc[0]["Start"]
    delta15 = obj15 - start15 - ausrueck
    
    ktwFMS16 = ktwFMS.loc[ktwFMS["KFZ"] == "'1-KTW-6'"]
    erste16 = ktwFMS16[0:1]
    obj16 = erste16.iloc[0]["Start"]
    delta16 = obj16 - start16 - ausrueck

    dfOut = pd.DataFrame({'KFZ(Funk)':['1-KTW-2', '1-KTW-3', '1-KTW-4', '1-KTW-5', '1-KTW-6'],
                           'Standzeit':[strfdelta(delta12, '{hours}:{minutes}'), 
                                        strfdelta(delta13, '{hours}:{minutes}'), 
                                        strfdelta(delta14, '{hours}:{minutes}'), 
                                        strfdelta(delta15, '{hours}:{minutes}'), 
                                        strfdelta(delta16, '{hours}:{minutes}')]})
    dfOut.to_csv(AUSWERTUNGFMS)


def auswertungStatistik(fahrtenStatistik):
    auswertung = fahrtenStatistik
    
    fahrten12 = auswertung[auswertung.KFZ == "'1-KTW-2'"].shape[0]
    iFahrten12 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-2'")].shape[0]
    fahrten13 = auswertung[auswertung.KFZ == "'1-KTW-3'"].shape[0]
    iFahrten13 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-3'")].shape[0]
    fahrten14 = auswertung[auswertung.KFZ == "'1-KTW-4'"].shape[0]
    iFahrten14 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-4'")].shape[0]
    fahrten15 = auswertung[auswertung.KFZ == "'1-KTW-5'"].shape[0]
    iFahrten15 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-5'")].shape[0]
    fahrten16 = auswertung[auswertung.KFZ == "'1-KTW-6'"].shape[0]
    iFahrten16 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-6'")].shape[0]

    dfOut = pd.DataFrame({'KFZ':["1-KTW-2", "1-KTW-3", "1-KTW-4", "1-KTW-5", "1-KTW-6"],
                          "Fahrten":[fahrten12, fahrten13, fahrten14, fahrten15, fahrten16],
                          "I-Fahrten":[iFahrten12, iFahrten13, iFahrten14, iFahrten15, iFahrten16]})
    dfOut.to_csv(AUSWERTUNGSTATISTIK)


data()    
ktwFMS(belegArchiv)
fahrtenStatistik(belegArchiv)
abrechnung(belegArchiv)
auswertungFMS(ktwFMS)
auswertungStatistik(fahrtenStatistik)


