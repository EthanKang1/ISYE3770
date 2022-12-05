import pandas as pd

from utils import csv2df


def getLapTimeStatsPerRace():

    # get lap times dataset
    lapTimesDataset = csv2df.convertDf("dataset/lap_times.csv")

    # get races dataset
    racesDataset = csv2df.convertDf("dataset/races.csv")

    # prune unnecessary columns
    lapTimesDataset.drop(['position', 'time'], axis=1, inplace=True)

    # split into dataframe per race
    lapTimesPerRace = dict(tuple(lapTimesDataset.groupby('raceId')))

    aggregate = []
    for index, raceDataset in lapTimesPerRace.items():
        tempDf = racesDataset.loc[racesDataset['raceId'] == index].copy()
        tempDf.drop(['name', 'date', 'time', 'url', 'fp1_date',
                              'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date',
                              'fp3_time', 'quali_date', 'quali_time', 'sprint_date',
                              'sprint_time'], axis=1, inplace=True)

        raceId = tempDf.iloc[0]['raceId']
        circuitId = tempDf.iloc[0]['circuitId']

        # print(circuitId)
        # print(raceDataset)
        statDf = raceDataset[["milliseconds"]].describe().T
        statDf.rename(index={'milliseconds': circuitId}, inplace=True)
        statDf.reset_index(inplace=True)
        statDf.rename(columns={'index': 'circuitId'}, inplace=True)
        statDf.insert(0, "raceId", raceId, True)

        aggregate.append(statDf)

    aggregateDf = pd.concat(aggregate)

    csv2df.outputDf(aggregateDf, "output/aggregateLapTimeStatsPerRace.csv")

getLapTimeStatsPerRace()
