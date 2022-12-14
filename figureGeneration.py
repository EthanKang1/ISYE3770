import pandas as pd
from utils import csv2df, utilFunc
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator
import matplotlib.ticker as ticker

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
        tempDf = tempDf.reindex(sorted(tempDf.columns), axis=1)
        # tempDf.reset_index(inplace=True)


        rotationDf = tempDf.T
        rotationDf.reset_index(inplace=True)

        rotationDf['year'] = rotationDf["index"].apply(lambda x: racesDataset.get(x)["year"])
        rotationDf.drop('index', axis=1, inplace=True)
        rotationDf = rotationDf.T
        rotationDf.columns = rotationDf.iloc[-1]
        rotationDf.drop(rotationDf.index[-1], inplace=True)
        tempDf = rotationDf

        # print(tempDf.columns)
        tempDf.columns = tempDf.columns.astype(int)

        # literally cannot be bothered, for some reason in 2020 there were two races on the same track
        try:
            tempDf = tempDf.reindex(sorted(tempDf.columns), axis=1)
        except:
            continue
        ax = tempDf.plot.box()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
        plt.show()
        ax.get_figure().savefig('figureOutput/byCircuit/' + uniqueCircuitName + '_lapTimeStats.jpg')

def correlationFiveOverTime():
    fastestLapSpeedDataset = csv2df.convertDf("regressionOutput/byYear/fastestLapSpeed.csv")
    fastestLapTimeDataset = csv2df.convertDf("regressionOutput/byYear/fastestLapTime.csv")
    gridDataset = csv2df.convertDf("regressionOutput/byYear/grid.csv")
    pitCountDataset = csv2df.convertDf("regressionOutput/byYear/pitCount.csv")
    pitTimeDataset = csv2df.convertDf("regressionOutput/byYear/pitTime.csv")

    df = gridDataset[['Year', 'grid_R2']].copy()
    df = pd.merge(df, fastestLapTimeDataset,  how='left', on=['Year'])
    df = pd.merge(df, fastestLapSpeedDataset,  how='left', on=['Year'])
    df = pd.merge(df, pitCountDataset,  how='left', on=['Year'])
    df = pd.merge(df, pitTimeDataset,  how='left', on=['Year'])

    df = df[['Year', 'grid_R2', 'fastestLapTime_R2', 'fastestLapSpeed_R2', 'pitCount_R2', 'pitTime_R2']]

    df.set_index('Year', inplace=True)
    df.sort_index(ascending=True, inplace=True)

    print(df)

    ax = df.plot.line()

    plt.show()
    ax.get_figure().savefig('figureOutput/correlationFactors.jpg')

correlationFiveOverTime()

