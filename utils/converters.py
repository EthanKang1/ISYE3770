import pandas as pd

# Takes in a series formatted as M:SS:lll
def convertDatetimeStrToMilli(series):
    seriesSplit = series.str.replace(':', '.').str.split('.', expand=True).astype(int)
    seriesTimeDelta = pd.to_timedelta(seriesSplit[0], unit='m') + pd.to_timedelta(seriesSplit[1], unit='s') + pd.to_timedelta(seriesSplit[2], unit='millisecond')
    milliseconds = (seriesTimeDelta.dt.total_seconds() * 1000).astype(int)

    return milliseconds.copy()