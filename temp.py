import sqlite3
import numpy as np
import csv

conn = sqlite3.connect('baseball.db')
c = conn.cursor()

with open('Pitcher and Hits.csv', 'rb') as f:
    reader = csv.reader(f)
    my_array = list(reader)

    for h in my_array:
        c.execute("""UPDATE 'Pitching' SET '1B%'=?, '2B%'=?, '3B%'=?, 'HR%'=? WHERE Name=?""", (h[1], h[2], h[3], h[4], h[0],))
        conn.commit()
