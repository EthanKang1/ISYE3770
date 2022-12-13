import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from sklearn import linear_model

from utils import csv2df, utilFunc

# add year as variable
# show correlation over time
# team performance over year
# driver performance correlated with age
# nationality correlation with performacne
# month born with performance
# probability of winning based off 1/2 stop (analyze historical and per circuit)

## factors that go into result
# correlations over time across multiple factors


## three circuits and factors
# average pit time, number of pits, fastest lap time, fastest speed, qualification
# three circuits
# get r^2
# get data for reach driver

## generate stat details for all factors

## all fives factors grouped by decade
## per year perf f



def positionCorrelation():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['grid'] != "\\N"]

    x = resultsDataset['position'].astype(float)
    y = resultsDataset['grid'].astype(float)

    historicalCorrelation(x, y, "regressionOutput/historical/gridCorrelation.png")

def fastestLapTimeCorrelation():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapTime'] != "\\N"]

    resultsDataset['fastestLapTime'] = utilFunc.convertDatetimeStrToMilli(resultsDataset['fastestLapTime'])

    x = resultsDataset['position'].astype(float)
    y = resultsDataset['fastestLapTime'].astype(float)

    historicalCorrelation(x, y, "regressionOutput/historical/fastestLapTimeCorrelation.png")

def fastestLapSpeedCorrelation():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapSpeed'] != "\\N"]

    x = resultsDataset['position'].astype(float)
    y = resultsDataset['fastestLapSpeed'].astype(float)

    historicalCorrelation(x, y, "regressionOutput/historical/fastestLapSpeedCorrelation.png")

def numOfPitCorrelation():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapSpeed'] != "\\N"]

    pitsDataset = utilFunc.getDataset("pit_stops")

    # build pit data
    driverPits = pd.DataFrame()
    uniqueRaces = pitsDataset['raceId'].unique().tolist()
    for uniqueRace in uniqueRaces:
        subset = pitsDataset[pitsDataset['raceId'] == uniqueRace]
        uniqueDrivers = subset['driverId'].unique().tolist()

        for uniqueDriver in uniqueDrivers:
            uniqueDriverPitCount = len(subset[subset['driverId'] == uniqueDriver])
            driverPits = driverPits.append({'raceId': uniqueRace, 'driverId': uniqueDriver, 'pitCount': uniqueDriverPitCount}, ignore_index = True)

    driverPits['raceId'] = driverPits['raceId'].astype(int)
    driverPits['driverId'] = driverPits['driverId'].astype(int)
    driverPits['pitCount'] = driverPits['pitCount'].astype(int)

    resultsDataset = pd.merge(resultsDataset, driverPits,  how='left', on=['raceId', 'driverId'])
    resultsDataset = resultsDataset[resultsDataset['pitCount'].notna()]

    x = resultsDataset['position'].astype(float)
    y = resultsDataset['pitCount'].astype(float)

    historicalCorrelation(x, y, "regressionOutput/historical/numOfPitCorrelation.png")

def pitTimeCorrelation():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapSpeed'] != "\\N"]

    pitsDataset = utilFunc.getDataset("pit_stops")

    # build pit data
    driverPitTime = pd.DataFrame()
    uniqueRaces = pitsDataset['raceId'].unique().tolist()
    for uniqueRace in uniqueRaces:
        subset = pitsDataset[pitsDataset['raceId'] == uniqueRace]
        uniqueDrivers = subset['driverId'].unique().tolist()

        for uniqueDriver in uniqueDrivers:
            uniqueDriverPitTime = subset[subset['driverId'] == uniqueDriver]['milliseconds'].sum()
            driverPitTime = driverPitTime.append({'raceId': uniqueRace, 'driverId': uniqueDriver, 'pitTime': uniqueDriverPitTime}, ignore_index = True)

    driverPitTime['raceId'] = driverPitTime['raceId'].astype(int)
    driverPitTime['driverId'] = driverPitTime['driverId'].astype(int)
    driverPitTime['pitTime'] = driverPitTime['pitTime'].astype(int)

    resultsDataset = pd.merge(resultsDataset, driverPitTime,  how='left', on=['raceId', 'driverId'])
    resultsDataset = resultsDataset[resultsDataset['pitTime'].notna()]

    x = resultsDataset['position'].astype(float)
    y = resultsDataset['pitTime'].astype(float)

    historicalCorrelation(x, y, "regressionOutput/historical/pitTimeCorrelation.png")

def positionCorrelationByYear():
    resultsDataset = utilFunc.getDataset("results")
    racesDataset = utilFunc.getDataset("races")

    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['grid'] != "\\N"]

    resultsDataset["year"] = resultsDataset["raceId"].apply(lambda x: racesDataset.get(x)["year"])

    correlationByYear('position', 'grid', resultsDataset)

def fastestLapTimeCorrelationByYear():
    resultsDataset = utilFunc.getDataset("results")
    racesDataset = utilFunc.getDataset("races")

    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapTime'] != "\\N"]

    resultsDataset['fastestLapTime'] = utilFunc.convertDatetimeStrToMilli(resultsDataset['fastestLapTime'])

    resultsDataset["year"] = resultsDataset["raceId"].apply(lambda x: racesDataset.get(x)["year"])

    correlationByYear('position', 'fastestLapTime', resultsDataset)

def fastestLapSpeedCorrelationByYear():
    resultsDataset = utilFunc.getDataset("results")
    racesDataset = utilFunc.getDataset("races")

    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapSpeed'] != "\\N"]

    resultsDataset["year"] = resultsDataset["raceId"].apply(lambda x: racesDataset.get(x)["year"])

    correlationByYear('position', 'fastestLapSpeed', resultsDataset)

def numOfPitCorrelationByYear():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapSpeed'] != "\\N"]

    racesDataset = utilFunc.getDataset("races")
    pitsDataset = utilFunc.getDataset("pit_stops")

    # build pit data
    driverPits = pd.DataFrame()
    uniqueRaces = pitsDataset['raceId'].unique().tolist()
    for uniqueRace in uniqueRaces:
        subset = pitsDataset[pitsDataset['raceId'] == uniqueRace]
        uniqueDrivers = subset['driverId'].unique().tolist()

        for uniqueDriver in uniqueDrivers:
            uniqueDriverPitCount = len(subset[subset['driverId'] == uniqueDriver])
            driverPits = driverPits.append({'raceId': uniqueRace, 'driverId': uniqueDriver, 'pitCount': uniqueDriverPitCount}, ignore_index = True)

    driverPits['raceId'] = driverPits['raceId'].astype(int)
    driverPits['driverId'] = driverPits['driverId'].astype(int)
    driverPits['pitCount'] = driverPits['pitCount'].astype(int)

    resultsDataset = pd.merge(resultsDataset, driverPits,  how='left', on=['raceId', 'driverId'])
    resultsDataset = resultsDataset[resultsDataset['pitCount'].notna()]

    resultsDataset["year"] = resultsDataset["raceId"].apply(lambda x: racesDataset.get(x)["year"])

    correlationByYear('position', 'pitCount', resultsDataset)

def pitTimeCorrelationByYear():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapSpeed'] != "\\N"]

    pitsDataset = utilFunc.getDataset("pit_stops")
    racesDataset = utilFunc.getDataset("races")

    # build pit data
    driverPitTime = pd.DataFrame()
    uniqueRaces = pitsDataset['raceId'].unique().tolist()
    for uniqueRace in uniqueRaces:
        subset = pitsDataset[pitsDataset['raceId'] == uniqueRace]
        uniqueDrivers = subset['driverId'].unique().tolist()

        for uniqueDriver in uniqueDrivers:
            uniqueDriverPitTime = subset[subset['driverId'] == uniqueDriver]['milliseconds'].sum()
            driverPitTime = driverPitTime.append({'raceId': uniqueRace, 'driverId': uniqueDriver, 'pitTime': uniqueDriverPitTime}, ignore_index = True)

    driverPitTime['raceId'] = driverPitTime['raceId'].astype(int)
    driverPitTime['driverId'] = driverPitTime['driverId'].astype(int)
    driverPitTime['pitTime'] = driverPitTime['pitTime'].astype(int)

    resultsDataset = pd.merge(resultsDataset, driverPitTime,  how='left', on=['raceId', 'driverId'])
    resultsDataset = resultsDataset[resultsDataset['pitTime'].notna()]

    resultsDataset["year"] = resultsDataset["raceId"].apply(lambda x: racesDataset.get(x)["year"])

    correlationByYear('position', 'pitTime', resultsDataset)

def historicalCorrelation(independent, dependent, filename):
    regr = linear_model.LinearRegression()
    regr.fit(independent.values.reshape(-1, 1), dependent)

    print('Intercept: \n', regr.intercept_)
    print('Coefficients: \n', regr.coef_)

    independent = sm.add_constant(independent)

    model = sm.OLS(dependent, independent).fit()
    predictions = model.predict(independent)

    print_model = model.summary()

    utilFunc.summaryToImage(print_model, filename)

# takes in a dataset with independent column, dependent column, and year
def correlationByYear(independent_name, dependent_name, dataset):

    coefficient = pd.DataFrame()

    for uniqueYear in utilFunc.getUniqueYears():
        subset = dataset[dataset["year"] == uniqueYear]

        x = subset[independent_name].astype(float)
        y = subset[dependent_name].astype(float)

        if (x.empty or y.empty):
            print(uniqueYear)
            continue

        regr = linear_model.LinearRegression()
        regr.fit(x.values.reshape(-1, 1), y)

        print('Intercept: \n', regr.intercept_)
        print('Coefficients: \n', regr.coef_)

        x = sm.add_constant(x)

        model = sm.OLS(y, x).fit()
        predictions = model.predict(x)

        coefficient = coefficient.append({'Year': uniqueYear, dependent_name + '_R2': model.rsquared, dependent_name + 'Coeff': regr.coef_[0], dependent_name + '_Inter': regr.intercept_}, ignore_index = True)

    print(coefficient)
    csv2df.outputDf(coefficient, "regressionOutput/byYear/" + dependent_name + ".csv")

pitTimeCorrelationByYear()