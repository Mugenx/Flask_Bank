from flask import Flask, render_template, g, request, redirect, url_for, session, flash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'wu'
app.database = "db/sample.db"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login_in' in session:
            return f(*args, **kwargs)
        else:
            flash('please login first.')
            return redirect(url_for('login'))

    return wrap


@app.route('/')
@login_required
def index():
    return "HELLO WORLD!"


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
    return render_template("login.html", error=error, isin=True)


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
        accountNum = 1101
        balance = 400
        interest = 0.1
        transactions = [["Nov 21 2016", "deposit", 50, 600],
                        ["Jan 2 2017", "Withdraw", 50, 550],
                        ["Feb 14 2017", "Withdraw", 150, 400]]
    else:
        accountNum = 2202
        balance = 100
        interest = 0.2
        transactions = [["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Nov 26 2016", "deposit", 10, 110],
                        ["Jan 30 2017", "Withdraw", 10, 100]]
    return render_template("account.html", type=type, accountNum=accountNum, balance=balance,
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


if __name__ == "__main__":
    app.run(debug=True)
