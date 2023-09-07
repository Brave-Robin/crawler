import sqlite3


# one = 'pew-pew'
# two = '$100500'
# third = 'n/a'

con = sqlite3.connect("ebay.sqlite")
cur = con.cursor()
cur.execute("CREATE TABLE storage(url, title, price, availability)")
# cur.execute("INSERT INTO storage VALUES ('Live Arcade Volume 1 for XBOX 360 - Includes 1 Month XBOX Live Gold subscription', '$100', 'none')")
# con.commit()
# for i in range(10000):
#     one = i
#     two = i + 1
#     third = i + 2
#     cur.execute("INSERT INTO storage (title, price, availability) VALUES (?, ?, ?)", (one, two, third))
# con.commit()
