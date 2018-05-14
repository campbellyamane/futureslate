import requests
from bs4 import BeautifulSoup
import sqlite3
import numpy as np

#updates stats, pulling from start of 2017 season through present
def update():
    hitters = requests.get("https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=150&type=c,34,35,36,23,37,38,39,40,60,41,42,43,44,45,46,47,48,49,7,8,9,10,11&season=2018&month=0&season1=2017&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_600")
    pitchers = requests.get("https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=50&type=c,120,121,217,41,43,45,46,47,48,49,50,51,52,53,11,114&season=2018&month=0&season1=2017&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_500")
    soup = BeautifulSoup(hitters.content, 'html.parser')

    conn = sqlite3.connect('baseball.db')
    c = conn.cursor()

    players = []
    for p1 in soup.findAll(True, {"class":["rgRow", "rgAltRow"]}):
        player = []
        hits = 0
        for n, stat in enumerate(p1.findAll("td")):
            if n != 0 and n != 2:
                s = stat.text
                if n == 21:
                    hits = float(s)
                else:
                    if n > 21:
                        player.append(float(s)/hits)
                    else:
                        if s[-2:] == " %":
                            s = float(s[:-2])/100
                        if n != 1:
                            s = float(s)
                        player.append(s)
        players.append(player)
    for p in players:
        p.insert(len(p)-1, p.pop(0))
    c.executemany("""UPDATE 'Hitting'
                      SET 'BB%'=?,
                      'K%'=?,
                      'BB/K'=?,
                      'AVG'=?,
                      'OBP'=?,
                      'SLG'=?,
                      'OPS'=?,
                      'ISO'=?,
                      'SPD'=?,
                      'BABIP'=?,
                      'GB/FB'=?,
                      'LD%'=?,
                      'GB%'=?,
                      'FB%'=?,
                      'IFFB%'=?,
                      'HR/FB'=?,
                      'IFH%'=?,
                      'BUH%'=?,
                      '1B%'=?,
                      '2B%'=?,
                      '3B%'=?,
                      'HR%'=?
                     WHERE Name=?;""",
                     players)
    conn.commit()

    #update league average
    c.execute('SELECT AVG("LD%"), AVG("FB%"), AVG("GB%"), AVG("IFFB%"), AVG("GIDP%"), AVG("FC%"), AVG("HO%"), AVG("1B%"), AVG("2B%"), AVG("3B%"), AVG("HR%") FROM Hitting')
    results = c.fetchone()
    c.execute("""UPDATE 'Hitting' SET 'LD%'=?, 'FB%'=?, 'GB%'=?, 'IFFB%'=?, 'GIDP%'=?, 'FC%'=?, 'HO%'=?, '1B%'=?, '2B%'=?, '3B%'=?, 'HR%'=? WHERE Team='MLB'""", (results[0], results[1], results[2], results[3], results[4], results[5], results[6], results[7], results[8], results[9], results[10],))
    conn.commit()

    pitchers = requests.get("https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=50&type=c,120,121,217,41,43,45,46,47,48,49,50,51,52,53,11,114&season=2018&month=0&season1=2017&ind=0&team=0&rost=0&age=0&filter=&players=0&page=1_500")
    soup = BeautifulSoup(pitchers.content, 'html.parser')

    players = []
    for p1 in soup.findAll(True, {"class":["rgRow", "rgAltRow"]}):
        player = []
        for n, stat in enumerate(p1.findAll("td")):
            if n != 0 and n != 2:
                s = stat.text
                if s[-2:] == " %":
                    s = float(s[:-2])/100
                if n != 1:
                    s = float(s)
                player.append(s)
        players.append(player)
    for p in players:
        p.insert(len(p)-1, p.pop(0))
    c.executemany("""UPDATE 'Pitching'
                      SET 'K%'=?,
                      'BB%'=?,
                      'K-BB%'=?,
                      'AVG'=?,
                      'BABIP'=?,
                      'FIP'=?,
                      'GB/FB'=?,
                      'LD%'=?,
                      'GB%'=?,
                      'FB%'=?,
                      'IFFB%'=?,
                      'HR/FB'=?,
                      'IFH%'=?,
                      'BUH%'=?,
                      'SV'=?,
                      'HLD'=?
                     WHERE Name=?;""",
                     players)
    conn.commit()
