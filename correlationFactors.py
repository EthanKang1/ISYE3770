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


def positionCorrelation():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['grid'] != "\\N"]

    x = resultsDataset['position'].astype(float)
    y = resultsDataset['grid'].astype(float)

    historicalCorrelation(x, y, "regressionOutput/historical/gridCorrelation.png")

def positionCorrelationByYear():
    resultsDataset = utilFunc.getDataset("results")
    racesDataset = utilFunc.getDataset("races")

    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['grid'] != "\\N"]

    resultsDataset["year"] = resultsDataset["raceId"].apply(lambda x: racesDataset.get(x)["year"])

    coefficient = pd.DataFrame()

    for uniqueYear in utilFunc.getUniqueYears():
        subset = resultsDataset[resultsDataset["year"] == uniqueYear]

        x = subset['position'].astype(float)
        y = subset['grid'].astype(float)

        regr = linear_model.LinearRegression()
        regr.fit(x.values.reshape(-1, 1), y)

        print('Intercept: \n', regr.intercept_)
        print('Coefficients: \n', regr.coef_)

        x = sm.add_constant(x)

        model = sm.OLS(y, x).fit()
        predictions = model.predict(x)

        coefficient = coefficient.append({'Year': uniqueYear, 'Grid_R2': model.rsquared, 'Grid_Coeff': regr.coef_[0], 'Grid_Inter': regr.intercept_}, ignore_index = True)

    print(coefficient)
    csv2df.outputDf(coefficient, "regressionOutput/byYear/grid.csv")

def fastestLapTimeCorrelationByYear():
    resultsDataset = utilFunc.getDataset("results")
    racesDataset = utilFunc.getDataset("races")

    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapTime'] != "\\N"]

    resultsDataset['fastestLapTime'] = utilFunc.convertDatetimeStrToMilli(resultsDataset['fastestLapTime'])

    resultsDataset["year"] = resultsDataset["raceId"].apply(lambda x: racesDataset.get(x)["year"])

    coefficient = pd.DataFrame()

    for uniqueYear in utilFunc.getUniqueYears():
        subset = resultsDataset[resultsDataset["year"] == uniqueYear]

        x = subset['position'].astype(float)
        y = subset['fastestLapTime'].astype(float)

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

        coefficient = coefficient.append({'Year': uniqueYear, 'FastestLapTime_R2': model.rsquared, 'FastestLapTime_Coeff': regr.coef_[0], 'FastestLapTime_Inter': regr.intercept_}, ignore_index = True)

    print(coefficient)
    csv2df.outputDf(coefficient, "regressionOutput/byYear/fastestLapTime.csv")

def fastestLapTimeCorrelation():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapTime'] != "\\N"]

    resultsDataset['fastestLapTime'] = utilFunc.convertDatetimeStrToMilli(resultsDataset['fastestLapTime'])

    x = resultsDataset['position'].astype(float)
    y = resultsDataset['fastestLapTime'].astype(float)

    historicalCorrelation(x, y, "regressionOutput/historical/fastestLapTimeCorrelation.png")

def fastestLapSpeedCorrelationByYear():
    resultsDataset = utilFunc.getDataset("results")
    racesDataset = utilFunc.getDataset("races")

    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapSpeed'] != "\\N"]

    resultsDataset["year"] = resultsDataset["raceId"].apply(lambda x: racesDataset.get(x)["year"])

    coefficient = pd.DataFrame()

    for uniqueYear in utilFunc.getUniqueYears():
        subset = resultsDataset[resultsDataset["year"] == uniqueYear]

        x = subset['position'].astype(float)
        y = subset['fastestLapSpeed'].astype(float)

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

        coefficient = coefficient.append({'Year': uniqueYear, 'FastestLapSpeed_R2': model.rsquared, 'FastestLapSpeed_Coeff': regr.coef_[0], 'FastestLapSpeed_Inter': regr.intercept_}, ignore_index = True)

    print(coefficient)
    csv2df.outputDf(coefficient, "regressionOutput/byYear/fastestLapSpeed.csv")

def fastestLapSpeedCorrelation():
    resultsDataset = utilFunc.getDataset("results")
    resultsDataset = resultsDataset[resultsDataset['position'] != "\\N"]
    resultsDataset = resultsDataset[resultsDataset['fastestLapSpeed'] != "\\N"]

    x = resultsDataset['position'].astype(float)
    y = resultsDataset['fastestLapSpeed'].astype(float)

    historicalCorrelation(x, y, "regressionOutput/historical/fastestLapSpeedCorrelation.png")

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

fastestLapSpeedCorrelationByYear()