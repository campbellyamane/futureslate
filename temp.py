import sqlite3
import numpy as np
import csv

conn = sqlite3.connect('baseball.db')
conn.text_factory = str
c = conn.cursor()

with open('lb.csv', 'rb') as f:
    reader = csv.reader(f)
    my_array = list(reader)

    for h in my_array:
        c.execute("""UPDATE 'Hitting' SET 'Team'=? WHERE Name=?""", (h[1], h[0],))
        conn.commit()
