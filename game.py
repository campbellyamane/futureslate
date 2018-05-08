from lineups import get_lineups, get_matchups
from outcomes import at_bat, steal
from update_stats import update
from set_new_scores import set_new_scores
import sys
import datetime
from datetime import timedelta
from dateutil import parser
import sys
import string

#for rookie callups or players who don't have data, they are defaulted to an average rookie's stats

default_hitter = ['name', 'team', 0.08,0.25,0.36,0.25,0.32,0.41,0.73,0.16,3.74,0.31,1.43,0.21,0.45,0.34,0.08,0.14,0.06,0.15,0.462290503,0.268918233,0.268791265,0.629984937,0.199210814,0.019963558,0.150840691]
default_pitcher = ['name', 'team', 0.22,0.09,0.12,0.25,0.29,4.52,1.42,0.20,0.44,0.36,0.11,0.14,0.06,0.18,0.30,3.08,0.462290503,0.268918233,0.268791265,0.629984937,0.199210814,0.019963558,0.150840691]

def start_game(lineups):
    #game variables
    away = lineups[0]
    home = lineups[1]
    away.append(matchups[int(pick)][0])
    home.append(matchups[int(pick)][1])
    away_stats = []
    home_stats = []
    league_stats = []


    #selects data for all players in lineup and puts it into an array
    for hitter in range (0,9):
        c.execute('SELECT * FROM Hitting WHERE Name=?', (away[hitter],))
        try:
            results = c.fetchone()
            len(results)
            away_stats.append(results)
        except:
            temp = default_hitter
            temp[0] = away[hitter]
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
    for hitter in range (0,9):
        c.execute('SELECT * FROM Hitting WHERE Name=?', (home[hitter],))
        try:
            results = c.fetchone()
            len(results)
            home_stats.append(results)
        except:
            temp = default_hitter
            temp[0] = home[hitter]
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

    c.execute('SELECT AVG("LD%"), AVG("GB%"), AVG("FB%"), AVG("IFFB%"), AVG("GIDP%"), AVG("FC%"), AVG("HO%"), AVG("1B%"), AVG("2B%"), AVG("3B%"), AVG("HR%") FROM Hitting')
    league_stats = c.fetchone()

    #keeps track of away vs home record when multiple simulations are being run for one matchup
    track = [0,0]

    #loops through matchup 1000 times to even out results
    for game in range(0, 5000):
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
                r = at_bat(batting[up], pitching, league_stats, bases, sit) #gets result of current at bat

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
                #print "\n" + home[10] + " win, " + str(score[1]) +" - " + str(score[0])
                track[1] += 1
                break
            elif inning >= 9 and not top and score[1] < score[0]:
                #print "\n" + away[10] + " win, " + str(score[0]) +" - " + str(score[1])
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
        print float(track[0])/5000
        return str(away[10])
    else:
        print home[10]
        print float(track[1])/5000
        return str(home[10])

#updates database stats, connects to sqlite database which uses fangraphs data from 2017-2018
import sqlite3
conn = sqlite3.connect('baseball.db')
c = conn.cursor()

c.execute('SELECT MAX(Day) FROM Results WHERE 1')
last_result = c.fetchone()[0]

yesterday = datetime.datetime.today() - timedelta(1)
yd =  yesterday.strftime('%Y-%m-%d')

#if yesterday's games have not been reported, update stats and results
if last_result != yd:
    update()
    set_new_scores(last_result)
    days_ago = 1
    print "Updating"
    #continue updating database with projections until it reaches the most recent projections
    while True:
        sim_date = datetime.datetime.today() - timedelta(days_ago)
        date_string =  sim_date.strftime('%Y-%m-%d')
        if date_string == last_result:
            break
        for pick in range(0, len(get_matchups(date_string)[0])):
            matchups = get_matchups(date_string)[0]
            lineups = get_lineups(pick, date_string)
            winner = start_game(lineups)
            c.execute('UPDATE Results SET Projected_Winner=? WHERE Day=? AND Away=? AND Home=?', (winner, date_string,lineups[0][10],lineups[1][10],))
            conn.commit()
        days_ago += 1

    print "Update Complete"
#allows user to select the matchup they want
matchups = get_matchups("")[0]
times = get_matchups("")[1]


while True:
    for i, m in enumerate(matchups):
        print str(i+1) + ". " + m[0] + " vs " + m[1] + " [" + times[i] + "]"
    print "\n"

    pick = int(raw_input("Which game would you like to simulate?\n"))-1
    lineups = get_lineups(pick, "")
    if len(lineups[0]) == 10 and len(lineups[1]) == 10:
        break
    else:
        print "\nThe lineups for the selected matchup have not been set yet. Please select a different matchup.\n*Lineups generally set around 3 hours before gametime\n"

start_game(lineups)
