import pandas as pd
from WinFraction import WinFraction

def createMarginMapping(df):
    margin_mapping = dict()

    for index, row in df.iterrows():
        home_score = row['Home Score']
        away_score = row['Away Score']
        home_margin = row['Home Line Close']
        away_margin = row['Away Line Close']

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
