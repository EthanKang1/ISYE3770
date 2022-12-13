import pandas as pd
from utils import csv2df, utilFunc

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

        csv2df.outputDf(subset, "tableOutput/byCircuit/" + uniqueCircuitName + "_lapTimeStats.csv")

    csv2df.outputDf(aggregateDf, "tableOutput/lapTimeStats_PerRace.csv")


getLapTimeStatsPerRace()
