import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import timedelta


PATHTXT = "exportArchiv.txt"
BELEGARCHIV = "data/belegArchiv.csv"
BELEGARCHIVONGOING = "data/belegArchivOngoing.csv"
KTWFMS = "data/ktwFMS.csv"
KTWFMSGOING = "data/ktwFMSOngoing.csv"
FAHRTENSTATISTIK = "data/fahrtenStatistik.csv"
ABRECHNUNG = "data/abrechnung.csv"
AUSWERTUNGFMS = "data/auswertungFMS.csv"
AUSWERTUNGFMSGOING = "data/auswertungFMSOngoing.csv"
AUSWERTUNGSTATISTIK = "data/auswertungStatistik.csv"
AUSWERTUNGSTATISTIKGOING = "data/auswertungStatistikOngoing.csv"
AUSWERTUNGFAHRTENMHD = "data/auswertungFahrtenMHD.csv"
AUSWERTUNGFAHRTENDRK = "data/auswertungFahrtenDRK.csv"

belegArchiv = None
dfOut = None

def strfdelta(timedelta, fmt):
    """
    Format für timedelta Objekte. Es werden nur Stunden und Minuten angezeigt
    """
    d = {'days': timedelta.days}
    d['hours'], rem = divmod(timedelta.seconds, 3600)
    d['minutes'], d['seconds'] = divmod(rem, 60)
    return(fmt.format(**d))

def data():
    """
    Konvertiert den .txt Exportiert aus dem Belegarchiv in .csv Datei
    """
    global belegArchiv
    data = pd.read_csv(PATHTXT, sep = ";", header = None, names = ["E-Datum", "Einsatz Nr.", "KFZ", "Transport von",
                                                                 "Transport nach", "Fahrgast", "Start", "Ende",
                                                                 "Infektion", "Tarifzone Num.", "Belegart", "Tarifzone"])
    data = data.iloc[1:]
    belegArchiv = pd.DataFrame(data)
    belegArchiv.to_csv(BELEGARCHIV, encoding = 'utf-8')
    writeToArchive(BELEGARCHIV, BELEGARCHIVONGOING)
    return(belegArchiv)

def ktwFMS(belegArchiv):
    """
    Erzeugt die DB für die Zeiterfassung,
    Parmeter: E-Datum, KFZ, Start, Ende,
    """
    global ktwFMS
    ktwFMS = belegArchiv[["E-Datum", "KFZ", "Start", "Ende"]]

    ktwFMS.to_csv(KTWFMS, encoding='utf-8')
    writeToArchive(KTWFMS, KTWFMSGOING)
    return(ktwFMS)

def fahrtenStatistik(belegArchiv):
    """
    Erzeugt die DB für die Fahrtenstatistik
    Parameter: E-Datum, KFZ, Transport nach, Infektion
    """
    global fahrtenStatistik
    fahrtenStatistik = belegArchiv[["E-Datum", "KFZ", "Transport nach", "Infektion", "Tarifzone"]]
   
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

def auswertungFMS(ktwFMS):
    """
    Erzeugt die Auswertungen der Standzeiten aus der ktwFMS DB
    """
    global auswertungFMS
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

    """
    Instanziere Dienstzeiten DRK 1-9
    TODO KTW 5-9 ist meistens der Nacht KTW hier aufpassen bei Fahrzuegwechsel
    """
    dienst52 = '06:00'
    start52 = dt.datetime.strptime(dienst52, '%H:%M')
    dienst53 = '06:30'
    start53 = dt.datetime.strptime(dienst53, '%H:%M')
    dienst54 = '07:00'
    start54 = dt.datetime.strptime(dienst54, '%H:%M')
    dienst55 = '08:30'
    start55 = dt.datetime.strptime(dienst55, '%H:%M')
    dienst56 = '09:30'
    start56 = dt.datetime.strptime(dienst56, '%H:%M')
    dienst57 = '08:30'
    start57 = dt.datetime.strptime(dienst57, '%H:%M')
    dienst58 = '09:30'
    start58 = dt.datetime.strptime(dienst58, '%H:%M')
    dienst59 = '19:45'
    start59 = dt.datetime.strptime(dienst59, '%H:%M')
    
    ktwFMS["Start"] = pd.to_datetime(ktwFMS["Start"], format = "'%H:%M'")
    ktwFMS.sort_values(by = ["KFZ", "Start"])

    #MHD
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

    #DRK
    ktwFMS52 = ktwFMS.loc[ktwFMS["KFZ"] == "'5-KTW-2'"]
    erste52 = ktwFMS52[0:1]
    obj52 = erste52.iloc[0]["Start"]
    delta52 = obj52 - start52 - ausrueck

    ktwFMS53 = ktwFMS.loc[ktwFMS["KFZ"] == "'5-KTW-3'"]
    erste53 = ktwFMS53[0:1]
    obj53 = erste53.iloc[0]["Start"]
    delta53 = obj53 - start53 - ausrueck

    ktwFMS54 = ktwFMS.loc[ktwFMS["KFZ"] == "'5-KTW-4'"]
    erste54 = ktwFMS54[0:1]
    obj54 = erste54.iloc[0]["Start"]
    delta54 = obj54 - start54 - ausrueck

    ktwFMS55 = ktwFMS.loc[ktwFMS["KFZ"] == "'5-KTW-5'"]
    erste55 = ktwFMS55[0:1]
    obj55 = erste55.iloc[0]["Start"]
    delta55 = obj55 - start55 - ausrueck

    ktwFMS56 = ktwFMS.loc[ktwFMS["KFZ"] == "'5-KTW-6'"]
    erste56 = ktwFMS56[0:1]
    obj56 = erste56.iloc[0]["Start"]
    delta56 = obj56 - start56 - ausrueck

    ktwFMS57 = ktwFMS.loc[ktwFMS["KFZ"] == "'5-KTW-7'"]
    erste57 = ktwFMS57[0:1]
    obj57 = erste57.iloc[0]["Start"]
    delta57 = obj57 - start57 - ausrueck

    ktwFMS58 = ktwFMS.loc[ktwFMS["KFZ"] == "'5-KTW-8'"]
    erste58 = ktwFMS58[0:1]
    obj58 = erste58.iloc[0]["Start"]
    delta58 = obj58 - start58 - ausrueck

    ktwFMS59 = ktwFMS.loc[ktwFMS["KFZ"] == "'5-KTW-9'"]
    erste59 = ktwFMS59[0:1]
    obj59 = erste59.iloc[0]["Start"]
    delta59 = obj59 - start59 - ausrueck

    auswertungFMS = pd.DataFrame({'KFZ(Funk)':['1-KTW-2', '1-KTW-3', '1-KTW-4', '1-KTW-5', '1-KTW-6', 
                                       '5-KTW-2', '5-KTW-3', '5-KTW-4', '5-KTW-5', '5-KTW-6', '5-KTW-7', '5-KTW-8', '5-KTW-9'],
                           'Standzeit':[strfdelta(delta12, '{hours}:{minutes}'), 
                                        strfdelta(delta13, '{hours}:{minutes}'), 
                                        strfdelta(delta14, '{hours}:{minutes}'), 
                                        strfdelta(delta15, '{hours}:{minutes}'), 
                                        strfdelta(delta16, '{hours}:{minutes}'),
                                        strfdelta(delta52, '{hours}:{minutes}'),
                                        strfdelta(delta53, '{hours}:{minutes}'),
                                        strfdelta(delta54, '{hours}:{minutes}'),
                                        strfdelta(delta55, '{hours}:{minutes}'),
                                        strfdelta(delta56, '{hours}:{minutes}'),
                                        strfdelta(delta57, '{hours}:{minutes}'),
                                        strfdelta(delta58, '{hours}:{minutes}'),
                                        strfdelta(delta59, '{hours}:{minutes}')]})
    auswertungFMS.to_csv(AUSWERTUNGFMS)
    writeToArchive(AUSWERTUNGFMS, AUSWERTUNGFMSGOING)
    return(auswertungFMS)

def auswertungStatistik(fahrtenStatistik):
    global auswertungStatistik 
    auswertung = fahrtenStatistik
      
    #MHD
    fahrten12 = auswertung[auswertung.KFZ == "'1-KTW-2'"].shape[0]
    iFahrten12 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-2'")].shape[0]
    fernKT12 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'1-KTW-2'")].shape[0]
    ktvp12 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'1-KTW-2'")].shape[0]
    fernfahrt12 = fernKT12 + ktvp12
    fahrten13 = auswertung[auswertung.KFZ == "'1-KTW-3'"].shape[0]
    iFahrten13 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-3'")].shape[0]
    fernKT13 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'1-KTW-3'")].shape[0]
    ktvp13 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'1-KTW-3'")].shape[0]
    fernfahrt13 = fernKT13 + ktvp13
    fahrten14 = auswertung[auswertung.KFZ == "'1-KTW-4'"].shape[0]
    iFahrten14 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-4'")].shape[0]
    fernKT14 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'1-KTW-4'")].shape[0]
    ktvp14 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'1-KTW-4'")].shape[0]
    fernfahrt14 = fernKT14 + ktvp14
    fahrten15 = auswertung[auswertung.KFZ == "'1-KTW-5'"].shape[0]
    iFahrten15 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-5'")].shape[0]
    fernKT15 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'1-KTW-5'")].shape[0]
    ktvp15 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'1-KTW-5'")].shape[0]
    fernfahrt15 = fernKT15 + ktvp15
    fahrten16 = auswertung[auswertung.KFZ == "'1-KTW-6'"].shape[0]
    iFahrten16 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'1-KTW-6'")].shape[0]
    fernKT16 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'1-KTW-6'")].shape[0]
    ktvp16 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'1-KTW-6'")].shape[0]
    fernfahrt16 = fernKT16 + ktvp16

    auswertungMHD = pd.DataFrame({'KFZ':["1-KTW-2", "1-KTW-3", "1-KTW-4", "1-KTW-5", "1-KTW-6"],
                          "Fahrten":[fahrten12, fahrten13, fahrten14, fahrten15, fahrten16],
                          "I-Fahrten":[iFahrten12, iFahrten13, iFahrten14, iFahrten15, iFahrten16],
                          "Fernfahrten":[fernfahrt12, fernfahrt13, fernfahrt14, fernfahrt15, fernfahrt16]})
    auswertungMHD.to_csv(AUSWERTUNGFAHRTENMHD)
    

    #DRK
    fahrten52 = auswertung[auswertung.KFZ == "'5-KTW-2'"].shape[0]
    iFahrten52 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'5-KTW-2'")].shape[0]
    fernKT52 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'5-KTW-2'")].shape[0]
    ktvp52 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'5-KTW-2'")].shape[0]
    fernfahrt52 = fernKT52 + ktvp52
    fahrten53 = auswertung[auswertung.KFZ == "'5-KTW-3'"].shape[0]
    iFahrten53 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'5-KTW-3'")].shape[0]
    fernKT53 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'5-KTW-3'")].shape[0]
    ktvp53 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'5-KTW-3'")].shape[0]
    fernfahrt53 = fernKT53 + ktvp53
    fahrten54 = auswertung[auswertung.KFZ == "'5-KTW-4'"].shape[0]
    iFahrten54 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'5-KTW-4'")].shape[0]
    fernKT54 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'5-KTW-4'")].shape[0]
    ktvp54 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'5-KTW-4'")].shape[0]
    fernfahrt54 = fernKT54 + ktvp54
    fahrten55 = auswertung[auswertung.KFZ == "'5-KTW-5'"].shape[0]
    iFahrten55 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'5-KTW-5'")].shape[0]
    fernKT55 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'5-KTW-5'")].shape[0]
    ktvp55 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'5-KTW-5'")].shape[0]
    fernfahrt55 = fernKT55 + ktvp55
    fahrten56 = auswertung[auswertung.KFZ == "'5-KTW-6'"].shape[0]
    iFahrten56 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'5-KTW-6'")].shape[0]
    fernKT56 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'5-KTW-6'")].shape[0]
    ktvp56 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'5-KTW-6'")].shape[0]
    fernfahrt56 = fernKT56 + ktvp56
    fahrten57 = auswertung[auswertung.KFZ == "'5-KTW-7'"].shape[0]
    iFahrten57 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'5-KTW-7'")].shape[0]
    fernKT57 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'5-KTW-7'")].shape[0]
    ktvp57 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'5-KTW-7'")].shape[0]
    fernfahrt57 = fernKT57 + ktvp57
    fahrten58 = auswertung[auswertung.KFZ == "'5-KTW-8'"].shape[0]
    iFahrten58 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'5-KTW-8'")].shape[0]
    fernKT58 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'5-KTW-8'")].shape[0]
    ktvp58 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'5-KTW-8'")].shape[0]
    fernfahrt58 = fernKT58 + ktvp58
    fahrten59 = auswertung[auswertung.KFZ == "'5-KTW-9'"].shape[0]
    iFahrten59 = auswertung[(auswertung["Infektion"] == "'J'") & (auswertung["KFZ"] == "'5-KTW-9'")].shape[0]
    fernKT59 = auswertung[(auswertung["Tarifzone"] == "'FERN-KT'") & (auswertung["KFZ"] == "'5-KTW-9'")].shape[0]
    ktvp59 = auswertung[(auswertung["Tarifzone"] == "'KTVP-FERN'") & (auswertung["KFZ"] == "'5-KTW-9'")].shape[0]
    fernfahrt59 = fernKT59 + ktvp59

    auswertungDRK = pd.DataFrame({'KFZ':["5-KTW-2", "5-KTW-3", "5-KTW-4", "5-KTW-5", "5-KTW-6", "5-KTW-7", "5-KTW-8", "5-KTW-9"],
                          "Fahrten":[fahrten52, fahrten53, fahrten54, fahrten55, fahrten56, fahrten57, fahrten58, fahrten59],
                          "I-Fahrten":[iFahrten52, iFahrten53, iFahrten54, iFahrten55, iFahrten56, iFahrten57, iFahrten58, iFahrten59],
                          "Fernfahrten":[fernfahrt52, fernfahrt53, fernfahrt54, fernfahrt55, fernfahrt56, fernfahrt57, fernfahrt58, fernfahrt59]})
    auswertungDRK.to_csv(AUSWERTUNGFAHRTENDRK)

    auswertungStatistik = pd.DataFrame({'KFZ':["1-KTW-2", "1-KTW-3", "1-KTW-4", "1-KTW-5", "1-KTW-6", 
                                 "5-KTW-2", "5-KTW-3", "5-KTW-4", "5-KTW-5", "5-KTW-6", "5-KTW-7", "5-KTW-8", "5-KTW-9"],
                          "Fahrten":[fahrten12, fahrten13, fahrten14, fahrten15, fahrten16,
                                     fahrten52, fahrten53, fahrten54, fahrten55, fahrten56, fahrten57, fahrten58, fahrten59],
                          "I-Fahrten":[iFahrten12, iFahrten13, iFahrten14, iFahrten15, iFahrten16,
                                       iFahrten52, iFahrten53, iFahrten54, iFahrten55, iFahrten56, iFahrten57, iFahrten58, iFahrten59],
                           "Fernfahrten":[fernfahrt12, fernfahrt13, fernfahrt14, fernfahrt15, fernfahrt16,
                                          fernfahrt52, fernfahrt53, fernfahrt54, fernfahrt55, fernfahrt56, fernfahrt57, fernfahrt58, fernfahrt59]})
    auswertungStatistik.to_csv(AUSWERTUNGSTATISTIK)
    writeToArchive(AUSWERTUNGSTATISTIK, AUSWERTUNGSTATISTIKGOING)
    return(auswertungStatistik)

def writeToArchive(readFile, writeFile):
    """
    Hängt die Tagesauswertung (readFile) an das Hauptarchiv (writeFile) an
    """
    #Lese aktuelles Belegarchiv
    dataNew = pd.read_csv(readFile, index_col=0)
    dataFrameNew = pd.DataFrame(dataNew)
    
    #Lese das weiterlaufende Belegarchiv
    dataOld = pd.read_csv(writeFile, index_col=0)
    dataFrameOld = pd.DataFrame(dataOld)

    dataFrameMerge = dataFrameOld.append(dataFrameNew, ignore_index = True, sort = False)
    dataFrameMerge.to_csv(writeFile, encoding = 'utf-8')





data()
ktwFMS(belegArchiv)
fahrtenStatistik(belegArchiv)
abrechnung(belegArchiv)
auswertungFMS(ktwFMS)
auswertungStatistik(fahrtenStatistik)
