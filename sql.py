import sqlite3  # import database module

with sqlite3.connect("db/sample.db") as connection:  # database connection
    c = connection.cursor()  # define cursor
    # c.execute("DROP TABLE transactions")  # Drop table
    # c.execute(  # Create table
    #     "CREATE TABLE transactions(accountNum INT, Date DATE, TransactionDescription TEXT, Action TEXT, Amount INT, Balance INT)")
    # c.execute('INSERT INTO transactions VALUES(1101, "2016-11-26", "payroll","deposit",100,100)')  # insert value
    # c.execute('INSERT INTO transactions VALUES(2202, "2017-02-14", "spend","withdraw",100,100)')

    # c.execute(
    #     'CREATE TABLE users ( userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, email TEXT )')
    # c.execute("INSERT INTO users (username,password,email) VALUES (?,?,?)", ('admin', 'admin', 'admin@flaskbank.com'))
    # c.execute("INSERT INTO users (username,password,email) VALUES (?,?,?)", ('saha', 'saha', 'saha@flaskbank.com'))
