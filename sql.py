import sqlite3

with sqlite3.connect("db/sample.db") as connection:
    c = connection.cursor()
    c.execute("DROP TABLE transactions")
    c.execute(
        "CREATE TABLE transactions(accountNum INT, Date DATE, TransactionDescription TEXT, Action TEXT, Amount INT, Balance INT)")
    c.execute('INSERT INTO transactions VALUES(1101, "2016-11-26", "payroll","deposit",100,100)')
    c.execute('INSERT INTO transactions VALUES(2202, "2017-02-14", "spend","withdraw",100,100)')

