import sqlite3
import numpy as np
import csv

conn = sqlite3.connect('baseball.db')
c = conn.cursor()

with open('Pitcher GIDP.csv', 'rb') as f:
    reader = csv.reader(f)
    my_array = list(reader)

    for h in my_array:
        c.execute("""UPDATE 'Pitching' SET 'GIDP%'=?, 'FC%'=?, 'HO%'=? WHERE Name=?""", (h[1], h[2], h[3], h[0],))
        conn.commit()
