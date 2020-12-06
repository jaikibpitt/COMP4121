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
