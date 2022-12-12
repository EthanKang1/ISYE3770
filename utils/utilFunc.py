import pandas as pd
from utils import csv2df
import matplotlib.pyplot as plt


# Takes in a series formatted as M:SS:lll
def convertDatetimeStrToMilli(series):
    seriesSplit = series.str.replace(':', '.').str.split('.', expand=True).astype(int)
    seriesTimeDelta = pd.to_timedelta(seriesSplit[0], unit='m') + pd.to_timedelta(seriesSplit[1], unit='s') + pd.to_timedelta(seriesSplit[2], unit='millisecond')
    milliseconds = (seriesTimeDelta.dt.total_seconds() * 1000).astype(int)

    return milliseconds.copy()


# Simplifies the dataset imports
def getDataset(dataset):

    output = None

    if dataset == "circuits":
        df = csv2df.convertDf("dataset/" + dataset + ".csv")[["circuitId",
                                                              "name",
                                                              "location",
                                                              "country"]]
        output = df.set_index('circuitId').T.to_dict()
    elif dataset == "drivers":
        df = csv2df.convertDf("dataset/" + dataset + ".csv")[["driverId",
                                                              "code",
                                                              "forename",
                                                              "surname",
                                                              "dob",
                                                              "nationality"]]
        output = df.set_index('driverId').T.to_dict()
    elif dataset == "lap_times":
        df = csv2df.convertDf("dataset/" + dataset + ".csv")[["raceId",
                                                              "driverId",
                                                              "lap",
                                                              "milliseconds"]]
        output = df.copy()
    elif dataset == "pit_stops":
        df = csv2df.convertDf("dataset/" + dataset + ".csv")[["raceId",
                                                              "driverId",
                                                              "stop",
                                                              "milliseconds"]]
        output = df.copy()
    elif dataset == "qualifying":
        df = csv2df.convertDf("dataset/" + dataset + ".csv")[["qualifyId",
                                                              "raceId",
                                                              "driverId",
                                                              "position"]]
        output = df.copy()
    elif dataset == "races":
        df = csv2df.convertDf("dataset/" + dataset + ".csv")[["raceId",
                                                              "year",
                                                              "circuitId",
                                                              "name"]]
        output = df.set_index('raceId').T.to_dict()
    elif dataset == "results":
        df = csv2df.convertDf("dataset/" + dataset + ".csv")[["resultId",
                                                              "raceId",
                                                              "driverId",
                                                              "grid",
                                                              "position",
                                                              "fastestLapTime",
                                                              "fastestLapSpeed"]]
        output = df.copy()

    return output

def summaryToImage(model, filename):
    plt.rc('figure', figsize=(12, 7))
    plt.text(0.01, 0.05, str(model), {'fontsize': 14}, fontproperties = 'monospace') # approach improved by OP -> monospace!
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)

def getUniqueYears():
    df = csv2df.convertDf("dataset/races.csv")
    output = df['year'].unique().tolist()

    return output
