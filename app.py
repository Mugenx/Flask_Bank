from flask import Flask, render_template, g, request, redirect, url_for, session, flash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'wu'
app.database = "db/sample.db"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login first')
            return redirect(url_for('login'))

    return wrap


@app.route('/')
@login_required
def index():
    return redirect(url_for('welcome'))


@app.route('/welcome')
def welcome():
    accountType = ["Chequing", "Saving"]
    return render_template("welcome.html", accountType=accountType)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('Welcome back')
            return redirect(url_for('welcome'))
    return render_template("login.html", error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('See you later')
    return redirect(url_for('login'))


@app.route("/profile")
def profile():
    name = 'wu'
    info = [
        ["Name:", name],
        ["email:", "%s@gmail.com" % name],
        ["address:", "algonquin college, Woodroffe, Ottawa, ON, CA"],
        ["phone:", 6130000000]
    ]
    return render_template("profile.html", name=name, info=info)


@app.route("/account/<type>")
def account(type):
    if type == "Chequing":
        account_num = 1101
        interest = 0.1
        balance, transactions = get_account_detail(account_num)
    else:
        account_num = 2202
        interest = 0.2
        balance, transactions = get_account_detail(account_num)
    return render_template("account.html", type=type, accountNum=account_num, balance=balance,
                           interest=interest,
                           transactions=transactions)


@app.route('/db')
def db_test():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM posts')
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('db.html', posts=posts)


def connect_db():
    return sqlite3.connect(app.database)


def get_account_detail(account_num):
    g.db = connect_db()
    cur = g.db.execute(
        'SELECT Balance FROM transactions WHERE accountNum = %s ORDER BY DATE DESC LIMIT 1' % account_num)
    balance = [dict(balance=row[0]) for row in cur.fetchall()]
    cur = g.db.execute('SELECT * FROM transactions WHERE accountNum = %s' % account_num)
    transactions = [dict(Date=row[1], TransactionDescription=row[2], Action=row[3], Amount=row[4], Balance=row[5])
                    for row in cur.fetchall()]
    g.db.close()
    return balance, transactions


if __name__ == "__main__":
    app.run(debug=True)
