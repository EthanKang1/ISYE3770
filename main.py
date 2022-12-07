import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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
    whiskerComp = {}
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

        whiskerDf = raceDataset[["milliseconds"]].copy()
        whiskerDf.reset_index(inplace=True, drop=True)
        whiskerDf.rename({'milliseconds': raceId}, axis="columns", inplace=True)

        if circuitId not in whiskerComp.keys():
            whiskerComp[circuitId] = pd.DataFrame()
        whiskerComp[circuitId][raceId] = whiskerDf[raceId]

        # print(whiskerComp)

        # whiskerDf.rename(columns={'index': 'circuitId'}, inplace=True)
        # whiskerComp
        # print(whiskerDf)

        # testing printing out box whisker plot


    aggregateDf = pd.concat(aggregate)


    # group by quali position
    uniqueCircuitIds = aggregateDf['circuitId'].unique().tolist()

    # print(uniqueCircuitIds)

    # for circuitId in uniqueCircuitIds:
    #     segmentDf = aggregateDf[aggregateDf["circuitId"] == circuitId].copy()
    #
    #     csv2df.outputDf(segmentDf, "output/circuitStatsOverTime/" + str(circuitId) + ".csv")


    for circuitId in whiskerComp.keys():
        tempDf = whiskerComp[circuitId]

        # tempDf[(np.abs(stats.zscore(tempDf)) < 3).all(axis=1)]

        Q1 = tempDf.quantile(0.25)
        Q3 = tempDf.quantile(0.75)
        IQR = Q3 - Q1

        tempDf = tempDf[~((tempDf < (Q1 - 1.5 * IQR)) |(tempDf > (Q3 + 1.5 * IQR))).any(axis=1)]

        ax = tempDf.plot.box()
        plt.show()
        ax.get_figure().savefig('output/circuitStatsOverTime/' + str(circuitId) + '.jpg')


    csv2df.outputDf(aggregateDf, "output/aggregateLapTimeStatsPerRace.csv")


def getPosDelta():

    # get datasets
    qualifyingDataset = csv2df.convertDf("dataset/qualifying.csv")
    resultsDataset = csv2df.convertDf("dataset/results.csv")

    qualifyingDataset.drop(['number', 'q1', 'q2', 'q3'], axis=1, inplace=True)
    qualifyingDataset.rename({'position': "qualifyingPosition"}, axis='columns', inplace=True)

    resultsDataset.drop(['number', 'positionText', 'positionOrder', 'points', 'laps',
                         'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime',
                         'fastestLapSpeed', 'statusId'], axis=1, inplace=True)
    resultsDataset.rename({'position': "resultPosition"}, axis='columns', inplace=True)

    newDf = pd.merge(resultsDataset, qualifyingDataset,  how='left', on=['raceId', 'driverId', 'constructorId'])

    # dataset cleaning
    newDf = newDf[newDf["qualifyingPosition"] != "\\N"]
    newDf = newDf[newDf["resultPosition"] != "\\N"]
    newDf = newDf[newDf["qualifyingPosition"].notnull()]
    newDf = newDf[newDf["resultPosition"].notnull()]

    newDf["qualifyingPosition"] = pd.to_numeric(newDf["qualifyingPosition"])
    newDf["resultPosition"] = pd.to_numeric(newDf["resultPosition"])
    newDf['PosDelta'] = newDf['resultPosition'].sub(newDf['qualifyingPosition'], axis = 0)

    csv2df.outputDf(newDf, "output/rawPositionDelta.csv")

    # group by quali position
    uniqueQualPositions = newDf['qualifyingPosition'].unique().tolist()
    for qualPos in uniqueQualPositions:
        segmentDf = newDf[newDf["qualifyingPosition"] == qualPos].copy()
        valueCountDf = segmentDf["resultPosition"].value_counts().to_frame()
        valueCountDf.reset_index(inplace=True)
        valueCountDf.rename({'index': "Starting Qualifying Position", "resultPosition": "Frequency of Resulting Position"}, axis='columns', inplace=True)
        valueCountDf.sort_values(by=['Starting Qualifying Position'], inplace=True)
        # print(valueCountDf)
        ax = valueCountDf.plot.bar(x='Starting Qualifying Position', y='Frequency of Resulting Position', rot=0)

        plt.show()
        ax.get_figure().savefig('output/positionDelta/qual_' + str(qualPos) + '.jpg')


def getPosPitImpact():

    # get datasets
    pitDataset = csv2df.convertDf("dataset/pit_stops.csv")
    resultsDataset = csv2df.convertDf("dataset/results.csv")

    # clean dataset
    pitDataset.drop(['lap', 'time', 'duration'], axis=1, inplace=True)
    # pitDataset.rename({'position': "qualifyingPosition"}, axis='columns', inplace=True)

    print(pitDataset)

    ## ONLY EVALUATING RACES WITH 1 PITSTOP, REMOVE RACES WITH >1 PIT
    segmentDf = pitDataset[pitDataset["stop"] != 1].copy()
    join = pd.merge(pitDataset, segmentDf, how='outer', on=['raceId', 'driverId'], indicator=True)
    print(join)

    testDf = join[join["_merge"] == "left_only"].copy()
    testDf.drop(['stop_x', 'stop_y', "milliseconds_y", '_merge'], axis=1, inplace=True)
    # testDf.rename({'s': "qualifyingPosition"}, axis='columns', inplace=True)


    csv2df.outputDf(testDf, "output/test.csv")


getLapTimeStatsPerRace()
