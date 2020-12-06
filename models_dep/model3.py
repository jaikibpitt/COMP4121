import pandas as pd
from sklearn.model_selection import train_test_split
import statistics
from math import copysign


def runSim(df):
    train_df, test_df = train_test_split(df, test_size=0.2)

    margin_mapping = createMarginMapping(train_df)

    cash = 1000
    bets = 0

    for index, row in test_df.iterrows():
        wager = 0

        home_score = row['Home Score']
        away_score = row['Away Score']
        home_odds = row['Home Odds Close']
        away_odds = row['Away Odds Close']
        home_margin = row['Home Line Open']
        away_margin = row['Away Line Open']

        if home_margin not in margin_mapping.keys() or away_margin not in margin_mapping.keys():
            continue

        home_win = (home_score>away_score)

        home_chance = margin_mapping[home_margin].getWinFraction()
        away_chance = margin_mapping[away_margin].getWinFraction()


        home_value = getKellyCriterion(home_chance, home_odds)
        away_value = getKellyCriterion(away_chance, away_odds)

        if home_value > 0:
            wager = cash*home_value
            bets += 1
            cash -= wager

            if home_win:
                cash += home_odds*wager

        if away_value > 0:
            wager = cash*away_value
            bets += 1
            cash -= wager

            if not home_win:
                cash += away_odds*wager

        cash = round(cash, 2)

    return cash

def readDF(path, epsilon):
    df = pd.read_excel(path)

    # Set Header
    header_row = 0
    df.columns = df.iloc[header_row]
    df = df.drop(header_row)
    df = df.reset_index(drop=True)

    df = df[['Home Score', 'Away Score', 'Home Odds Close', 'Away Odds Close', 'Home Line Open', 'Away Line Open']]

    df = df.dropna()

    df['Home Line Open'] = df['Home Line Open'].astype(int)
    df['Away Line Open'] = df['Away Line Open'].astype(int)

    all_lines = pd.Series(dtype='float64')
    all_lines = all_lines.append(df['Home Line Open'])
    all_lines = all_lines.append(df['Away Line Open'])
    all_lines = all_lines.abs()

    stdev = all_lines.std()
    epsilon_limit = round(stdev*epsilon)
    print(epsilon_limit)

    df['Home Line Open'] = df['Home Line Open'].apply(lambda x: x if abs(x)<epsilon_limit else copysign(epsilon_limit,x))
    df['Away Line Open'] = df['Away Line Open'].apply(lambda x: x if abs(x)<epsilon_limit else copysign(epsilon_limit,x))

    return df

def createMarginMapping(df):
    margin_mapping = dict()

    for index, row in df.iterrows():
        home_score = row['Home Score']
        away_score = row['Away Score']
        home_margin = row['Home Line Open']
        away_margin = row['Away Line Open']

        if home_margin not in margin_mapping.keys():
            h_wf = WinFraction()
        else:
            h_wf = margin_mapping[home_margin]

        if away_margin not in margin_mapping.keys():
            a_wf = WinFraction()
        else:
            a_wf = margin_mapping[away_margin]

        if home_score > away_score:
            h_wf.addWin()
            a_wf.addLoss()
        elif home_score < away_score:
            h_wf.addLoss()
            a_wf.addWin()
        else:
            h_wf.addDraw()
            a_wf.addDraw()

        margin_mapping[home_margin] = h_wf
        margin_mapping[away_margin] = a_wf

    return margin_mapping

leagues = ['afl','nbl','nrl','super_rugby']

def getReturns(path, n):
    df = readDF(path,0.5)

    sum = 0
    l = list()
    for i in range(n):
        l.append(runSim(df))

    return l

for l in leagues:
    returns = getReturns('./'+l+'.xlsx', 1000)

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
