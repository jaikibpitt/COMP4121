import pandas as pd
from math import copysign


def readDF_Epsilon(path, epsilon):
    df = readDF(path)

    df['Home Line Open'] = df['Home Line Open'].astype(int)
    df['Away Line Open'] = df['Away Line Open'].astype(int)

    all_lines = pd.Series(dtype='float64')
    all_lines = all_lines.append(df['Home Line Open'])
    all_lines = all_lines.append(df['Away Line Open'])
    all_lines = all_lines.abs()

    stdev = all_lines.std()
    epsilon_limit = round(stdev*epsilon)

    df['Home Line Open'] = df['Home Line Open'].apply(lambda x: x if abs(x)<epsilon_limit else copysign(epsilon_limit,x))
    df['Away Line Open'] = df['Away Line Open'].apply(lambda x: x if abs(x)<epsilon_limit else copysign(epsilon_limit,x))

    all_lines = pd.Series(dtype='float64')
    all_lines = all_lines.append(df['Home Line Close'])
    all_lines = all_lines.append(df['Away Line Close'])
    all_lines = all_lines.abs()

    stdev = all_lines.std()
    epsilon_limit = round(stdev*epsilon)

    df['Home Line Close'] = df['Home Line Close'].apply(lambda x: x if abs(x)<epsilon_limit else copysign(epsilon_limit,x))
    df['Away Line Close'] = df['Away Line Close'].apply(lambda x: x if abs(x)<epsilon_limit else copysign(epsilon_limit,x))


    return df

def readDF(path):
    df = pd.read_excel(path)

    # Set Header
    header_row = 0
    df.columns = df.iloc[header_row]
    df = df.drop(header_row)
    df = df.reset_index(drop=True)

    df = df[['Home Score', 'Away Score', 'Home Odds Max', 'Away Odds Max', 'Home Line Open', 'Away Line Open', 'Home Line Close', 'Away Line Close']]

    df = df.dropna()

    return df

def readDF_Log(path):
    df = pd.read_excel(path)

    # Set Header
    header_row = 0
    df.columns = df.iloc[header_row]
    df = df.drop(header_row)
    df = df.reset_index(drop=True)

    df = df.assign(Win=df.apply(lambda x: int(x['Home Score']>x['Away Score']), axis=1))

    df = df.drop(columns=['Home Score', 'Away Score', 'Date','Kick-off (local)','Home Team','Away Team','Play Off Game?','Over Time?','Bookmakers Surveyed','Notes'])


    df = df.dropna()

    return df
