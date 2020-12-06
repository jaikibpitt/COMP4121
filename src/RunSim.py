from KellyCriterion import getKellyCriterion

def runSim(df, chanceModel):
    cash = 10000

    vision = False

    for index, row in df.iterrows():
        wager = 0

        home_score = row['Home Score']
        away_score = row['Away Score']
        home_odds = row['Home Odds Max']
        away_odds = row['Away Odds Max']
        home_margin = row['Home Line Close']
        away_margin = row['Away Line Close']

        home_win = (home_score>away_score)

        # home_chance = chanceModel.getChance(home_margin)
        # away_chance = chanceModel.getChance(away_margin)
        home_chance = chanceModel.getChanceLinear(home_margin)
        away_chance = chanceModel.getChanceLinear(away_margin)

        home_value = getKellyCriterion(home_chance, home_odds)
        away_value = getKellyCriterion(away_chance, away_odds)

        if home_value > 0:
            wager = round(cash*home_value,2)
            cash -= wager

            if home_win:
                cash += home_odds*wager

            if vision:
                print('Home')
                print('Margin: '+str(home_margin))
                print('Chance: '+str(home_chance))
                print('Odds: '+str(home_odds))
                print('Kelly: '+str(home_value))
                print('Wager: '+str(wager))
                print('Win: '+str(home_win))
                print('Cash: '+str(cash))
                print('==========')


        if away_value > 0:
            wager = round(cash*away_value,2)
            cash -= wager

            if not home_win:
                cash += away_odds*wager

            if vision:
                print('Away')
                print('Margin: '+str(away_margin))
                print('Chance: '+str(away_chance))
                print('Odds: '+str(away_odds))
                print('Kelly: '+str(away_value))
                print('Wager: '+str(wager))
                print('Win: '+str(not home_win))
                print('Cash: '+str(cash))
                print('==========')

        cash = round(cash, 2)

    return cash
