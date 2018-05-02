import matplotlib.pyplot as plt
from mpldatacursor import datacursor

#updates database stats, connects to sqlite database which uses fangraphs data from 2017-2018
import sqlite3
conn = sqlite3.connect('baseball.db')
c = conn.cursor()
c.execute('SELECT * FROM Results WHERE 1')
total = c.fetchall()

dates = []
games = []
correct = []
percentage = []

for i, t in enumerate(total):
    if t[0] not in dates:
        dates.append(t[0])
        games.append(1)
        correct.append(0)
        if (t[3] == t[4]):
            correct[len(correct)-1] += 1

    else:
        games[len(games)-1] += 1
        if (t[3] == t[4]):
            correct[len(correct)-1] += 1
for i, g in enumerate(games):
    percentage.append(float(correct[i])/games[i])

print float(sum(correct))/sum(games)
plt.ylim([0,1])
plt.plot(dates,percentage,'-o')
plt.show()
