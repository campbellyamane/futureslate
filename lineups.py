import requests
from bs4 import BeautifulSoup

#uses baseballpress.com to grab starting lineups and pitchers

#both functions now take date strings as arguments as to update the database with earlier projections

#creates an array of away vs home matchups for the day
def get_matchups(d):
    if d == "":
        r = requests.get("http://www.baseballpress.com/lineups")
        soup = BeautifulSoup(r.content, 'html.parser')
    else:
        r = requests.get("http://www.baseballpress.com/lineups/" + str(d))
        soup = BeautifulSoup(r.content, 'html.parser')
    matchups = []
    times = []
    h = ""
    a = ""
    for team in soup.findAll("div", class_="team-name"):
        if a == "":
            a = team.text
        elif h == "":
            h = team.text
        else:
            matchups.append([a,h])
            h = ""
            a = team.text
    matchups.append([a,h])

    #gets gametimes as well
    for time in soup.findAll("div", class_="game-time"):
        times.append(time.text)

    return [matchups, times]

#takes in the game that you want to simulate and returns home and away roster arrays
def get_lineups(x, d):
    if d == "":
        r = requests.get("http://www.baseballpress.com/lineups")
        soup = BeautifulSoup(r.content, 'html.parser')
    else:
        r = requests.get("http://www.baseballpress.com/lineups/" + str(d))
        soup = BeautifulSoup(r.content, 'html.parser')
    count = 0
    home = []
    away = []
    for lu in soup.findAll("div", class_="game clearfix"):
        if int(x) == count:
            for div in lu.findAll("div", class_="cssDialog clearfix"):
                for t in div.findAll("div", class_="team-lineup clearfix"):
                    for players in t.findAll("div", class_="players"):
                        for p in players.findAll("div"):
                            for n in p.findAll("a"):
                                if len(away) < 9: #as long as there's less than 9 hitters, keep adding. sometimes it starts adding from other teams, so I had to set a stopper
                                    away.append(n.text)
                                elif len(home) < 9:
                                    home.append(n.text) #once away team is finished, do home team
            #add pitchers
            for div in lu.findAll("div", class_="clearfix"):
                for pitch in div.findAll("div", class_="team-data"):
                    for players in pitch.findAll("div", class_="text"):
                        for p in players.findAll("div"):
                            for n in p.findAll("a"):
                                if len(away) == 9:
                                    away.append(n.text)
                                elif len(home) == 9:
                                    home.append(n.text)
        else:
            count += 1
    return [away, home]
