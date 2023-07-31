import sqlite3


con = sqlite3.connect("ebay.sqlite")
cur = con.cursor()
# cur.execute("CREATE TABLE storage(title, price, availability)")
cur.execute("INSERT INTO storage VALUES ('Live Arcade Volume 1 for XBOX 360 - Includes 1 Month XBOX Live Gold subscription', '$100', 'none')")
con.commit()