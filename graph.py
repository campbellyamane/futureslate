import matplotlib.pyplot as plt
from mpldatacursor import datacursor
import datetime
import numpy as np

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
    d = t[0].split("-")
    temp_date = datetime.date(int(d[0]), int(d[1]), int(d[2]))
    if temp_date not in dates:
        dates.append(temp_date)
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
fig = plt.figure()
ax = fig.gca()
ax.set_yticks(np.arange(0, 1.1, 0.1))
plt.ylim([0,1])
ax.yaxis.grid()
plt.plot_date(dates,percentage,'-o')
plt.show()
