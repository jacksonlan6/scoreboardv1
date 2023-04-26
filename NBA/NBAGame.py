

class NBAGame:
    def __init__(self, visitor, home, startTime, gameId, status, visitorScore, homeScore, winner):
        self.gameId = gameId
        self.visitor = visitor
        self.home = home
        self.startTime = startTime
        if (status == "Finished"):
            self.status = 1
            self.visitorScore = visitorScore
            self.homeScore = homeScore
            self.winner = winner
        elif (status == "In Play"):
            self.status = 2
            self.visitorScore = visitorScore
            self.homeScore = homeScore
        else:
            self.status = 3


