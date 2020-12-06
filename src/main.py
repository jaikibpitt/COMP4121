import statistics
from ReadDF import readDF_Epsilon, readDF
from RunSim import runSim
import pandas as pd
from ChanceModel import ChanceModel
from sklearn.model_selection import train_test_split
from MarginMapping import createMarginMapping
from time import time


leagues = ['afl','nbl','nrl','super_rugby']

def getReturns(path, df, n):
    sum = 0
    l = list()

    for i in range(n):
        train_df, test_df = train_test_split(df, test_size=0.2)
        margin_mapping = createMarginMapping(train_df)
        chanceModel = ChanceModel(margin_mapping)
        chanceModel.fitRegression()

        l.append(runSim(test_df, chanceModel))

    return l

std_map = {
    'afl' : 2,
    'nbl' : 1.75,
    'nrl' : 2,
    'super_rugby' :1.5
}

for l in leagues:
    path = '../data/'+l+'.xlsx'

    df = readDF_Epsilon(path,std_map[l])
    # df = readDF(path)

    returns = getReturns('./data/'+l+'.xlsx', df, 100)

    mean = statistics.mean(returns)
    median = statistics.median(returns)
    stdev = statistics.stdev(returns)
    max_ret = max(returns)
    min_ret = min(returns)

    print(l)
    print('Mean: '+str(mean))
    print('Median: '+str(median))
    print('STDEV: '+str(stdev))
    print('Max: '+str(max_ret))
    print('Min: '+str(min_ret))
