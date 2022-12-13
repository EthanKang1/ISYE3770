import pandas as pd
from utils import csv2df, utilFunc
import matplotlib.pyplot as plt

def getLapTimeStatsPerRace():

    # get datasets
    lapTimesDataset = csv2df.convertDf("dataset/lap_times.csv")
    racesDataset = csv2df.convertDf("dataset/races.csv")
    betterRacesDataset = utilFunc.getDataset("races")
    circuitsDataset = utilFunc.getDataset("circuits")

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

    aggregateDf = pd.concat(aggregate)

    ### whisker plot
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

    aggregateDf["year"] = aggregateDf["raceId"].apply(lambda x: betterRacesDataset.get(x)["year"])

    uniqueCircuits = aggregateDf['circuitId'].unique().tolist()

    for uniqueCircuit in uniqueCircuits:
        subset = aggregateDf[aggregateDf["circuitId"] == uniqueCircuit]
        uniqueCircuitName = circuitsDataset[uniqueCircuit]["name"].replace(" ", "")

        # table generation
        csv2df.outputDf(subset, "tableOutput/byCircuit/" + uniqueCircuitName + "_lapTimeStats.csv")

    csv2df.outputDf(aggregateDf, "tableOutput/lapTimeStats_PerRace.csv")

def topDriversPerCircuit():
    resultsDataset = utilFunc.getDataset("results")
    racesDataset = utilFunc.getDataset("races")
    circuitsDataset = utilFunc.getDataset("circuits")

    resultsDataset["circuitId"] = resultsDataset["raceId"].apply(lambda x: racesDataset.get(x)["circuitId"])

    uniqueCircuits = resultsDataset['circuitId'].unique().tolist()

    for uniqueCircuit in uniqueCircuits:
        subset = resultsDataset[resultsDataset["circuitId"] == uniqueCircuit]
        uniqueCircuitName = circuitsDataset[uniqueCircuit]["name"].replace(" ", "")
        uniqueDrivers = subset['driverId'].unique().tolist()
        driverPlacementDf = pd.DataFrame(uniqueDrivers, columns=['driverId'])
        driverPlacementDf["placements"] = ""

        uniqueRaces = subset['raceId'].unique().tolist()
        for uniqueRace in uniqueRaces:
            subsubset = subset[subset["raceId"] == uniqueRace][['driverId', 'position']]
            subsubset = subsubset[subsubset["position"] != '\\N']
            driverPlacementDf = pd.merge(driverPlacementDf, subsubset,  how='left', on=['driverId']).fillna("")
            driverPlacementDf["placements"] = driverPlacementDf["placements"] + "," + driverPlacementDf["position"]
            driverPlacementDf.drop('position', axis=1, inplace=True)

        for pos in range(1, 25):
            driverPlacementDf["pos_" + str(pos)] = driverPlacementDf["placements"].str.count("," + str(pos) + ",")
        driverPlacementDf.drop('placements', axis=1, inplace=True)

        csv2df.outputDf(driverPlacementDf, "tableOutput/byCircuit/placements/" + uniqueCircuitName + "_placements.csv")


topDriversPerCircuit()
