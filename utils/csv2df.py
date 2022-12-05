import pandas as pd

def convertDf(filename):
    df = pd.read_csv(filename)

    return df

def outputDf(df, filename):
    df.to_csv(filename, sep='\t', index=False)