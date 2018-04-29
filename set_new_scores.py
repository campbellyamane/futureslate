import requests
from lxml import html
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
from dateutil import parser
import sys
import string

def set_new_scores(last_result):
    yesterday = datetime.datetime.today() - timedelta(1)
    yd =  yesterday.strftime('%Y-%m-%d')

    r = requests.get("https://www.baseball-reference.com/leagues/MLB-schedule.shtml")
    soup = BeautifulSoup(r.content, 'html.parser')

    cities = ['Baltimore ','Arizona ','Boston ','Atlanta ','Chicago ','Cleveland ','Cincinnati ','Detroit ','Colorado ','Houston ', 'Los Angeles ','Kansas City ','Miami ','Milwaukee ','Minnesota ','New York ','Philadelphia ','Oakland ','Pittsburgh ','Seattle ','San Diego ','Tampa Bay ','San Francisco ','Texas ','St. Louis ','Toronto ','Washington ']
    update = []
    cont = False

    #scapes baseball reference for scores
    for score in soup.findAll("div", class_="section_content"):
        for game in score.findAll("div"):
            date = ""
            for date in game.findAll("h3"):
                try:
                    dt = parser.parse(str(date.text))
                    date = dt.strftime('%Y-%m-%d')
                except:
                    cont = False
            if cont:
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
            if last_result == date:
                cont = True
            if yd == date:
                break
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

    #adding results to database
    import sqlite3
    conn = sqlite3.connect('baseball.db')
    c = conn.cursor()

    for u in update:
        if len(u) == 4:
            c.execute('INSERT INTO Results(Day, Away, Home, Real_Winner) Values(?,?,?,?)', (u[0],u[1],u[2],u[3],))
            conn.commit()
