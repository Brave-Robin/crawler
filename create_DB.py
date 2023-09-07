import sqlite3

con = sqlite3.connect("ebay.sqlite")
cur = con.cursor()
cur.execute("CREATE TABLE storage(url, title, price, availability)")
