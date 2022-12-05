import pandas as pd

def convertDf(filename):
    df = pd.read_csv(filename)

    return df

def outputDf(df, filename):
    df.to_csv(filename, encoding='utf-8', index=False)