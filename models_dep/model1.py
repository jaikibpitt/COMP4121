import pandas as pd
from sklearn.model_selection import train_test_split
import statistics

class WinFraction:
    def __init__(self):
        self.wins = 0
        self.games = 0

    def addDraw(self):
        self.games += 1
        self.wins += 0.5

    def addLoss(self):
        self.games += 1

    def addWin(self):
        self.games += 1
        self.wins += 1

    def getWinFraction(self):
        return self.wins/self.games

def getKellyCriterion(success_chance, payout):
    try:
        ret = success_chance-((1-success_chance)/(payout-1))
    except ZeroDivisionError as err:
        # print(payout)
        ret = 0.5

    return ret

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

def readDF(path):
    df = pd.read_excel(path)

    # Set Header
    header_row = 0
    df.columns = df.iloc[header_row]
    df = df.drop(header_row)
    df = df.reset_index(drop=True)

    df = df[['Home Score', 'Away Score', 'Home Odds Close', 'Away Odds Close', 'Home Line Open', 'Away Line Open']]
    df = df.dropna()

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
    df = readDF(path)

    sum = 0
    l = list()
    for i in range(n):
        l.append(runSim(df))

    return l

print('Model 1:')
for l in leagues:
    returns = getReturns('./'+l+'.xlsx', 1000)

    mean = statistics.mean(returns)
    stdev = statistics.stdev(returns)
    max_ret = max(returns)
    min_ret = min(returns)

    print(l)
    print('Mean: '+str(mean))
    print('STDEV: '+str(stdev))
    print('Max: '+str(max_ret))
    print('Min: '+str(min_ret))
