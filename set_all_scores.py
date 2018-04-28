import requests
from lxml import html
from bs4 import BeautifulSoup
import datetime
from dateutil import parser
import sys
import string

#date =  datetime.datetime.today().strftime('%Y-%m-%d')

r = requests.get("https://www.baseball-reference.com/leagues/MLB-schedule.shtml")
soup = BeautifulSoup(r.content, 'html.parser')

#creates an array of away vs home matchups for the day
cities = ['Baltimore ','Arizona ','Boston ','Atlanta ','Chicago ','Cleveland ','Cincinnati ','Detroit ','Colorado ','Houston ', 'Los Angeles ','Kansas City ','Miami ','Milwaukee ','Minnesota ','New York ','Philadelphia ','Oakland ','Pittsburgh ','Seattle ','San Diego ','Tampa Bay ','San Francisco ','Texas ','St. Louis ','Toronto ','Washington ']
update = []
cont = True
for score in soup.findAll("div", id="div_6219322505"):
    for game in score.findAll("div"):
        date = ""
        for date in game.findAll("h3"):
            try:
                dt = parser.parse(str(date.text))
                date = dt.strftime('%Y-%m-%d')
            except:
                cont = False
        for matchups in game.findAll("p"):
            insert = []
            insert.append(date)
            for i, teams in enumerate(matchups.findAll("a")):
                if i == 0 or i == 1:
                    insert.append(teams.text)
            for winner in matchups.findAll("strong"):
                for w in winner.findAll("a"):
                    insert.append(w.text)

            update.append(insert)
        if not cont:
            break
for i,r in enumerate(update):
    try:
        for c in cities:
            update[i][1] = r[1].replace(c,"")
            update[i][2] = r[2].replace(c,"")
            update[i][3] = r[3].replace(c,"")

        update[i][1] = r[1].replace("D'Backs", "Diamondbacks")
        update[i][2] = r[2].replace("D'Backs", "Diamondbacks")
        update[i][3] = r[3].replace("D'Backs", "Diamondbacks")
    except:
        'ha'
import sqlite3
conn = sqlite3.connect('baseball.db')
c = conn.cursor()

for u in update:
    if len(u) == 4:
        c.execute('INSERT INTO Results(Day, Away, Home, Real_Winner) Values(?,?,?,?)', (u[0],u[1],u[2],u[3],))
        conn.commit()
