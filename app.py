from flask import Flask, render_template, g, request, redirect, url_for, session, flash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'wu'  # for session
app.database = "db/sample.db"  # define the database


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
    return "Flask Bank"


@app.route('/welcome')
def welcome():
    if session['logged_in'] is True:
        username = session['username']
        userid = get_user_id(username)
        accounts = get_user_accounts(userid)
        return render_template("welcome.html", username=username, accounts=accounts)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            error = 'Username and Password required. Please try again'
        else:
            g.db = connect_db()
            cur = g.db.execute('SELECT password FROM users WHERE username = "%s"' % username)
            pwd = cur.fetchone()[0]
            g.db.close()
            print(username)
            print(pwd)
            if password != pwd:
                error = 'Invalid credentials. Please try again'
            else:
                session['logged_in'] = True
                # flash('Welcome to Flask Bank')
                session['username'] = username
                return redirect(url_for('welcome'))
    return render_template("login.html", error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('See you later')
    return redirect(url_for('login'))


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == 'post':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        province = request.form['province']
        postcode = request.form['postcode']

        with sqlite3.connect(app.database) as con:
            cur = con.cursor()
        cur.execute(
            'INSERT INTO users (username, password, firstName, lastName, email, phone, address,city, province,postcode ) VALUES (?,?,?,?,?,?,?,?,?,?)',
            (username, password, firstName, lastName, email, phone, address, city, province, postcode))
        con.commit()
        con.close()
    return render_template('reg.html')


@app.route("/profile")
def profile():
    username = session['username']
    results = get_user_detail(username)
    return render_template("profile.html", results=results, username=username)


@app.route("/account/<account_num>")
def account(account_num):
    interest = 0.1
    type, balance, transactions = get_account_detail(account_num)
    if len(transactions) == 0:
        transactions = 0
    return render_template("account.html", type=type, accountNum=account_num, balance=balance,
                           interest=interest,
                           transactions=transactions)


@app.route('/transfer')
def transfer():
    return render_template('transfer.html')


@app.route('/newAccount')
def new_account():
    return render_template('newAccount.html')


def connect_db():
    return sqlite3.connect(app.database)


def get_user_id(username):
    g.db = connect_db()
    cur = g.db.execute('SELECT userid FROM users WHERE username = "%s"' % username)
    userid = cur.fetchone()[0]
    g.db.close()
    print(userid)
    return userid


def get_user_accounts(userid):
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM accounts WHERE userid = "%s" ORDER BY type' % userid)
    accounts = [dict(accountNum=row[1], type=row[2]) for row in cur.fetchall()]
    g.db.close()
    print(accounts)
    return accounts


def get_account_detail(account_num):
    g.db = connect_db()
    cur = g.db.execute(
        'SELECT type FROM accounts WHERE accountNum = %s' % account_num)
    type = cur.fetchone()[0]
    cur = g.db.execute(
        'SELECT Balance FROM transactions WHERE accountNum = %s ORDER BY DATE DESC LIMIT 1' % account_num)
    balance = [dict(balance=row[0]) for row in cur.fetchall()]
    cur = g.db.execute('SELECT * FROM transactions WHERE accountNum = %s' % account_num)
    transactions = [dict(Date=row[1], TransactionDescription=row[2], Action=row[3], Amount=row[4], Balance=row[5])
                    for row in cur.fetchall()]
    g.db.close()
    return type, balance, transactions


def get_user_detail(username):
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM users WHERE username = "%s"' % username)
    results = cur.fetchall()
    g.db.close()
    return results


g
if __name__ == "__main__":
    app.run(debug=True)
