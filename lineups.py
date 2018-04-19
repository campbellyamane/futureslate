import requests
from lxml import html
from bs4 import BeautifulSoup

r = requests.get("http://www.baseballpress.com/lineups")
soup = BeautifulSoup(r.content, 'html.parser')

matchups = []

def get_matchups():
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
    return matchups

def get_lineups(x):
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
                                if len(away) < 9:
                                    away.append(n.text)
                                elif len(home) < 9:
                                    home.append(n.text)
            for div in lu.findAll("div", class_="clearfix"):
                for pitch in div.findAll("div", class_="team-data"):
                    for players in pitch.findAll("div", class_="text"):
                        for p in players.findAll("div"):
                            for n in p.findAll("a"):
                                if len(away) < 10:
                                    away.append(n.text)
                                elif len(home) < 10:
                                    home.append(n.text)
        else:
            count += 1
    return [away, home]
