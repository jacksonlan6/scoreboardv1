import http.client
import json
from datetime import date
from flask import Flask
from flask import render_template, url_for
from NBA.NBATeamsDict import NBATeamDict as NBATeams
from NBA.NBAGame import NBAGame as NBAGameClass
import time


app = Flask(__name__)



today = date.today()

s =today.strftime('%Y-%m-%d')
time.sleep(10)

with open('BasketballTeams.json', 'r') as fp:
    teamsjson = json.load(fp)

teamLib = json.loads(teamsjson)


conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")

headers = {
    'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com",
   'X-RapidAPI-Key': "b000ca23a4mshddcbd4524667073p1d4364jsnef1cddc8cc67"
    }

conn.request("GET", "/games?date=2022-04-23", headers=headers)

res = conn.getresponse()
data = res.read()

jsongames = data.decode("utf-8")



with open('Games.json', 'w') as f:
    json.dump(jsongames, f, ensure_ascii=False, indent=4)

with open('Games.json', 'r') as fp:
    gamesjson = json.load(fp)

gamesLib = json.loads(gamesjson)
NBAGamesToday = len(gamesLib["response"])


i = 0
NBAGames = {}

while i <= NBAGamesToday - 1:
    NBAVisitor = NBATeams[gamesLib["response"][i]["teams"]["visitors"]["id"]]
    NBAHome = NBATeams[gamesLib["response"][i]["teams"]["home"]["id"]]
    GameId = gamesLib["response"][i]["id"]
    #time is like 5 ahead of est so need to make that change
    NBAgameStart = gamesLib["response"][i]["date"]["start"]
    gameStatus = gamesLib["response"][i]["status"]["long"]
    visScore = gamesLib["response"][i]["scores"]["visitors"]["points"]
    homeScor = gamesLib["response"][i]["scores"]["home"]["points"]
    output = ""
    if (visScore != "null" and gameStatus == 1):
        if (visScore > homeScor):
            output = 1
        else:
            output = 2

    
    g = NBAGameClass(NBAVisitor, NBAHome, NBAgameStart, GameId, str(gameStatus), visScore, homeScor, output)

    NBAGames[i] = g
    i += 1

CurrentNBAGames = {}

z = 0


@app.route('/')
@app.route('/NBAhomepage')
def index():
    return render_template('NBAhomepage.html', len = NBAGamesToday - 1, NBAGames = NBAGames)

if __name__ == '__main__':
   app.run()


