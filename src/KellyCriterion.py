def getKellyCriterion(success_chance, payout):
    if payout-1 == 0:
        ret = 0
    else:
        ret = success_chance-((1-success_chance)/(payout-1))

    return ret
