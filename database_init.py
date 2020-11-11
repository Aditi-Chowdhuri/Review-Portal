import sqlite3
conn = sqlite3.connect("database.db")

conn.execute("CREATE TABLE user(username text, email text, password text)")
conn.execute("CREATE TABLE review(field1 text, review text)")