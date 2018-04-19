from lineups import get_lineups, get_matchups
from outcomes import at_bat, steal

#connects to sqlite database which uses fangraphs data from 2017-2018
import sqlite3
conn = sqlite3.connect('baseball.db')
c = conn.cursor()

matchups = get_matchups()
for i, m in enumerate(matchups):
    print str(i+1) + ". " + m[0] + " vs " + m[1]
print "\n"

#allows user to select the matchup they want
pick = int(raw_input("Which game would you like to simulate?\n"))-1
lineups = get_lineups(pick)

#for rookie callups or players who don't have data, they are defaulted to a league average player's stats
default_hitter = ['name', 'team', 'pos', 0.09,0.22,0.40,0.25,0.32,0.42,0.75,0.17,4.38,0.30,1.25,0.20,0.44,0.36,0.10,0.14,0.07,0.28, 000]
default_pitcher = ['name', 'team', 0.22,0.09,0.13,0.25,0.30,4.32,1.25,0.20,0.44,0.36,0.10,0.14,0.07,0.28, 0, 0, 000]

#game variables
away = lineups[0]
home = lineups[1]
away.append(matchups[int(pick)][0])
home.append(matchups[int(pick)][1])
away_stats = []
home_stats = []


#selects data for all players in lineup and puts it into an array
for x in range (0,9):
    c.execute('SELECT * FROM Hitting WHERE Name=?', (away[x],))
    try:
        results = c.fetchone()
        len(results)
        away_stats.append(results)
    except:
        temp = default_hitter
        temp[0] = away[x]
        temp[1] = away[10]
        away_stats.append(temp)

c.execute('SELECT * FROM Pitching WHERE Name=?', (away[9],))

try:
    results = c.fetchone()
    len(results)
    away_stats.append(results)
except:
    temp = default_pitcher
    temp[0] = away[9]
    temp[1] = away[10]
    away_stats.append(temp)
for x in range (0,9):
    c.execute('SELECT * FROM Hitting WHERE Name=?', (home[x],))
    try:
        results = c.fetchone()
        len(results)
        home_stats.append(results)
    except:
        temp = default_hitter
        temp[0] = home[x]
        temp[1] = home[10]
        home_stats.append(temp)

c.execute('SELECT * FROM Pitching WHERE Name=?', (home[9],))
try:
    results = c.fetchone()
    len(results)
    home_stats.append(results)
except:
    temp = default_pitcher
    temp[0] = home[9]
    temp[1] = home[10]
    home_stats.append(temp)

#keeps track of away vs home record when multiple simulations are being run for one matchup
track = [0,0]

#loops through matchup 1000 times to even out results
for x in range(0, 1000):
    batting = [] #hitting team's stats array
    inning = 1
    top = True
    outs = 0
    score = [0,0] #away and home score
    spot = [0,0] #away and home position in batting order
    up = 0 #current spot in current lineup
    bases = ["","",""] #information about runners on base
    while True:
        #setup inning
        if top:
            batting = away_stats
            pitching = home_stats[9]
            up = spot[0]
            #print "\nTop " + str(inning) + "\n"
        else:
            batting = home_stats
            pitching = away_stats[9]
            up = spot[1]
            #print "\nBottom " + str(inning) + "\n"
        outs = 0
        bases = ["","",""]

        #setup at at_bats
        while outs < 3:
            sit = [inning, outs, top, score] #the current situation
            r = at_bat(batting[up], pitching, bases, sit) #gets result of current at bat

            #uses return values to update outs, score, and baserunners
            if r[0] == -1:
                outs += 1
            elif r[0] == -2:
                outs += 2
            if top and outs < 3:
                score[0] += r[2]
            elif outs < 3:
                score[1] += r[2]
            bases = r[1]

            #goes to next batter, back to top if at end
            if up < 8:
                up += 1
            else:
                up = 0

            #if in a potential steal situation, call steal function to determine if there was an attempt and if the attempt was successful
            if bases[1] == "" and bases[0] != "":
                r = steal(bases[0], bases, 0)
                bases = r[1]
                outs += r[0]
            elif bases[2] == "" and bases[1] != "":
                r = steal(bases[1], bases, 1)
                bases = r[1]
                outs += r[0]

        #post-inning cleanups

        #check for winner
        if inning >= 9 and top and score[1] > score[0]:
            print "\n" + home[10] + " win, " + str(score[1]) +" - " + str(score[0])
            track[1] += 1
            break
        elif inning >= 9 and not top and score[1] < score[0]:
            print "\n" + away[10] + " win, " + str(score[0]) +" - " + str(score[1])
            track[0] += 1
            break

        #update inning
        if top:
            top = False
            spot[0] = up
        else:
            top = True
            spot[1] = up
            inning += 1

#prints winningest team and their victory count
if track[0] > track[1]:
    print away[10]
    print track[0]
else:
    print home[10]
    print track[1]
