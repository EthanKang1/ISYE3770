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

def yearCorrelation():
    resultsDataset = utilFunc.getDataset("results")
    print(resultsDataset)

yearCorrelation()