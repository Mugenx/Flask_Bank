import sqlite3

with sqlite3.connect("db/sample.db") as connection:
    c = connection.cursor()
    c.execute("DROP TABLE posts")
    c.execute("CREATE TABLE posts(title TEXT, description TEXT)")
    c.execute('INSERT INTO posts VALUES("GOOD", "I am good")')
    c.execute('INSERT INTO posts VALUES("WELL", "I am well")')
