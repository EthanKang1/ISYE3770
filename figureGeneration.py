import pandas as pd
from utils import csv2df, utilFunc
import matplotlib.pyplot as plt

def createLapTimeStatsFigures():
    # get datasets
    lapTimesDataset = utilFunc.getDataset("lap_times")
    racesDataset = utilFunc.getDataset("races")
    circuitsDataset = utilFunc.getDataset("circuits")

    # add race id to lapTimesDataset
    lapTimesDataset["circuitId"] = lapTimesDataset["raceId"].apply(lambda x: racesDataset.get(x)["circuitId"])

    uniqueCircuits = lapTimesDataset['circuitId'].unique().tolist()

    for uniqueCircuit in uniqueCircuits:
        uniqueCircuitName = circuitsDataset[uniqueCircuit]["name"].replace(" ", "")
        subset = lapTimesDataset[lapTimesDataset["circuitId"] == uniqueCircuit]
        uniqueRaces = subset['raceId'].unique().tolist()

        tempDf = pd.DataFrame()
        for uniqueRace in uniqueRaces:
            subsubset = subset[subset["raceId"] == uniqueRace]["milliseconds"]
            subsubset = subsubset.reset_index(drop=True)
            tempDf[uniqueRace] = subsubset

        Q1 = tempDf.quantile(0.25)
        Q3 = tempDf.quantile(0.75)
        IQR = Q3 - Q1

        tempDf = tempDf[~((tempDf < (Q1 - 1.5 * IQR)) |(tempDf > (Q3 + 1.5 * IQR))).any(axis=1)]
        print(tempDf)

        ax = tempDf.plot.box()
        plt.show()
        ax.get_figure().savefig('figureOutput/byCircuit/' + uniqueCircuitName + '_lapTimeStats.jpg')

    # aggregate = []
    # whiskerComp = {}
    # for index, raceDataset in lapTimesPerRace.items():
    #     tempDf = racesDataset.loc[racesDataset['raceId'] == index].copy()
    #     tempDf.drop(['name', 'date', 'time', 'url', 'fp1_date',
    #                  'fp1_time', 'fp2_date', 'fp2_time', 'fp3_date',
    #                  'fp3_time', 'quali_date', 'quali_time', 'sprint_date',
    #                  'sprint_time'], axis=1, inplace=True)
    #
    #     raceId = tempDf.iloc[0]['raceId']
    #     circuitId = tempDf.iloc[0]['circuitId']
    #
    #     statDf = raceDataset[["milliseconds"]].describe().T
    #     statDf.rename(index={'milliseconds': circuitId}, inplace=True)
    #     statDf.reset_index(inplace=True)
    #     statDf.rename(columns={'index': 'circuitId'}, inplace=True)
    #     statDf.insert(0, "raceId", raceId, True)
    #
    #     aggregate.append(statDf)
    #
    #     whiskerDf = raceDataset[["milliseconds"]].copy()
    #     whiskerDf.reset_index(inplace=True, drop=True)
    #     whiskerDf.rename({'milliseconds': raceId}, axis="columns", inplace=True)
    #
    #     if circuitId not in whiskerComp.keys():
    #         whiskerComp[circuitId] = pd.DataFrame()
    #     whiskerComp[circuitId][raceId] = whiskerDf[raceId]
    #
    # aggregateDf = pd.concat(aggregate)

    # uniqueCircuits = circuitsDataset['circuitId'].unique().tolist()
    #
    # ## whisker plot
    # for circuitId in whiskerComp.keys():
    #     tempDf = whiskerComp[circuitId]
    #
    #     Q1 = tempDf.quantile(0.25)
    #     Q3 = tempDf.quantile(0.75)
    #     IQR = Q3 - Q1
    #
    #     tempDf = tempDf[~((tempDf < (Q1 - 1.5 * IQR)) |(tempDf > (Q3 + 1.5 * IQR))).any(axis=1)]
    #
    #     ax = tempDf.plot.box()
    #     plt.show()
    #     ax.get_figure().savefig('output/circuitStatsOverTime/' + str(circuitId) + '.jpg')


createLapTimeStatsFigures()
