import sqlite3

conn = sqlite3.connect("streetlight.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE street_light
SET pole_number = 'P104'
WHERE light_id = 'sl104'
""")

conn.commit()
conn.close()

print("Pole number updated successfully")