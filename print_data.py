import sqlite3
con = sqlite3.connect("database.db")
c = con.cursor()
c.execute("SELECT * FROM arduino_data")
print(c.fetchall())
