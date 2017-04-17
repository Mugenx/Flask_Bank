"""
Created on March 7th, 2017
last modified: April 17th 2017

@author: Guobin Wu
version: 1.0.1
professor: Stanley Pieda
filename: app.py

description: a bank system with using flask web framework
"""

# import modules
from datetime import date

from flask import Flask, render_template, g, request, redirect, url_for, session, flash
from functools import wraps  # import modules
import sqlite3  # import modules

app = Flask(__name__)
app.secret_key = 'wu'  # key for session
app.database = "db/sample.db"  # define the database


def login_required(f):  # login required function, controlling redirection
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login first')
            return redirect(url_for('login'))

    return wrap  # end for login_required


@app.route('/')
@login_required
def index():  # index page
    return "Flask Bank"


@app.route('/welcome')  # welcome page, displaying user accounts info
def welcome():
    if session['logged_in'] is True:  # if the user logged in then redirect to the welcome page
        username = session['username']
        userid = get_user_id(username)
        session['userid'] = userid
        accounts = get_user_accounts(userid)
        for item in accounts:
            item['sub'] = get_balance(item['accountNum'])
        print(accounts)
        return render_template("welcome.html", username=username, accounts=accounts)
    else:  # if not logged in, redirect to login page again.
        return redirect(url_for('login'))
        # end of welcome page


@app.route('/login', methods=['GET', 'POST'])
def login():  # login function
    error = None
    if request.method == 'POST':  # set method is post
        username = request.form['username']  # fetch username from input
        password = request.form['password']  # fetch password from input
        if username == '' or password == '':  # if can not fetch username of password, error message display
            error = 'Username and Password required. Please try again'
        else:  # if username and password are filled. search if the user is in the system
            g.db = connect_db()
            cur = g.db.execute(
                'SELECT password FROM users WHERE username = "%s"' % username)
            pwd = cur.fetchone()[0]
            g.db.close()
            print(username)
            print(pwd)
            if password != pwd:
                # if password invalid, error message display
                error = 'Invalid credentials. Please try again'
            else:  # if everything correct, user logged in, redirect to welcome page.
                session['logged_in'] = True
                # flash('Welcome to Flask Bank')
                session['username'] = username  # store username in session
                return redirect(url_for('welcome'))
    return render_template("login.html", error=error)  # end of login


@app.route('/logout')
@login_required
def logout():  # logout function
    session.pop('logged_in', None)
    flash('See you later')  # flash message
    return redirect(url_for('login'))  # redirect to login page. end of logout


@app.route("/profile")
def profile():  # profile function
    if session['logged_in'] is True:
        username = session['username']  # get username from session
        # fetch user details by calling get_user_detail function
        results = get_user_detail(username)
        # end of profile
        return render_template("profile.html", results=results, username=username)
    else:  # if not logged in, redirect to login page again.
        return redirect(url_for('login'))


@app.route("/account/<account_num>")
def account(account_num):  # account function
    interest = 0.1
    username = session['username']
    type, transactions = get_account_detail(
        account_num)  # fetch account type, balance and transactions by calling get_account_detail function
    balance = get_balance(account_num)
    if len(transactions) == 0:
        transactions = 0
    return render_template("account.html", username=username, type=type, accountNum=account_num, balance=balance,
                           interest=interest,
                           transactions=transactions)  # end of account


@app.route("/account/Chequing")
def account_chequing():  # account function
    if session['logged_in'] is True:  # if the user logged in then redirect to the welcome page
        username = session['username']
        userid = session['userid']
        accounts = get_chequing(userid)
        total = 0
        for item in accounts:
            item['sub'] = get_balance(item['accountNum'])
            total += item['sub']
        return render_template("chequing.html", username=username, accounts=accounts, total=total)
    else:  # if not logged in, redirect to login page again.
        return redirect(url_for('login'))
        # end of welcome page


@app.route("/account/Saving")
def account_saving():  # account function
    if session['logged_in'] is True:  # if the user logged in then redirect to the welcome page
        username = session['username']
        userid = session['userid']
        accounts = get_saving(userid)
        total = 0
        for item in accounts:
            item['sub'] = get_balance(item['accountNum'])
            total += item['sub']
        return render_template("Saving.html", username=username, accounts=accounts, total=total)
    else:  # if not logged in, redirect to login page again.
        return redirect(url_for('login'))
        # end of welcome page


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():  # transfer function, to be develop
    if session['logged_in'] is True:
        if request.method == 'POST':  # set method is post
            from_num = request.form['select']
            to_num = request.form['num']
            amount = request.form['amount']
            description = request.form['description']
            to_transfer(from_num, to_num, amount, description)
            return redirect(url_for('welcome'))
        username = session['username']
        userid = session['userid']
        accounts = get_user_accounts(userid)
        for item in accounts:
            item['sub'] = get_balance(item['accountNum'])
        return render_template('transfer.html', username=username, accounts=accounts)
    else:  # if not logged in, redirect to login page again.
        return redirect(url_for('login'))


@app.route('/newAccount')
def new_account():  # add new account function, to be develop:
    if session['logged_in'] is True:
        username = session['username']
        return render_template('newAccount.html', username=username)
    else:  # if not logged in, redirect to login page again.
        return redirect(url_for('login'))


@app.route('/newAccount/<type>')
def create_account(type):  # add new account function, to be develop
    if session['logged_in'] is True:
        userid = session['userid']
        create_new_account(userid, type)
        flash('New %s Account Was Created' % type)
        return redirect(url_for('welcome'))
    else:  # if not logged in, redirect to login page again.
        return redirect(url_for('login'))


@app.route('/delete_account/<accountNum>')
def delete_account(accountNum):
    if session['logged_in'] is True:
        g.db = connect_db()  # g object call connect database function
        cur = g.db.cursor()
        cur.execute(  # sql query to fetch data
            'DELETE FROM accounts WHERE accountNum = %s' % accountNum)
        cur.execute(  # sql query to fetch data
            'DELETE FROM transactions WHERE accountNum = %s' % accountNum)
        g.db.commit()
        g.db.close()  # close database connection
        flash('An Account Was Deleted')
        return redirect(url_for('welcome'))
    else:  # if not logged in, redirect to login page again.
        return redirect(url_for('login'))


def connect_db():  # initializing database connection
    return sqlite3.connect(app.database)


def get_user_id(username):  # get user id function.
    g.db = connect_db()  # g object call connect database function
    cur = g.db.execute(
        'SELECT userid FROM users WHERE username = "%s"' % username)  # sql query to fetch data from table
    userid = cur.fetchone()[0]  # store the data to variable
    g.db.close()  # close database connection
    return userid  # end of get user id


def get_user_accounts(userid):  # get user account function
    g.db = connect_db()  # g object call connect database function
    cur = g.db.execute(
        'SELECT * FROM accounts WHERE userid = "%s" ORDER BY type' % userid)  # sql query to fetch data from table
    accounts = [dict(accountNum=row[1], type=row[2])
                for row in cur.fetchall()]  # array to store data
    g.db.close()  # close database connection
    return accounts  # end of get user accounts function


def get_chequing(userid):
    g.db = connect_db()  # g object call connect database function
    cur = g.db.execute(
        'SELECT * FROM accounts WHERE userid = %s AND type = "Chequing"' % userid)  # sql query to fetch data from table
    accounts = [dict(accountNum=row[1], type=row[2])
                for row in cur.fetchall()]  # array to store data
    g.db.close()  # close database connection
    print(accounts)
    return accounts  # end of get user accounts function


def get_saving(userid):
    g.db = connect_db()  # g object call connect database function
    cur = g.db.execute(
        'SELECT * FROM accounts WHERE userid = %s AND type = "Saving"' % userid)  # sql query to fetch data from table
    accounts = [dict(accountNum=row[1], type=row[2])
                for row in cur.fetchall()]  # array to store data
    g.db.close()  # close database connection
    print(accounts)
    return accounts  # end of get user accounts function


def get_accounts(userid, type):
    g.db = connect_db()  # g object call connect database function
    cur = g.db.execute(
        'SELECT * FROM accounts WHERE userid = %s AND type = "%s"' % (
            userid, type))  # sql query to fetch data from table
    accounts = [dict(accountNum=row[1], type=row[2])
                for row in cur.fetchall()]  # array to store data
    g.db.close()  # close database connection
    return accounts  # end of get user accounts function


def get_account_detail(account_num):  # get account detail function
    g.db = connect_db()  # g object call connect database function
    cur = g.db.execute(  # sql query to fetch data
        'SELECT type FROM accounts WHERE accountNum = %s' % account_num)
    type = cur.fetchone()[0]  # store  the account type
    cur = g.db.execute('SELECT * FROM transactions WHERE accountNum = %s' %
                       account_num)  # sql query to fetch dat
    transactions = [dict(Date=row[2], TransactionDescription=row[3], Action=row[4], Amount=row[5], Balance=row[6])
                    for row in cur.fetchall()]  # array to store transactions
    g.db.close()  # close database connection
    return type, transactions  # return 3 results, end of account detail


def get_user_detail(username):  # get user detail function
    g.db = connect_db()  # g object call connect function
    cur = g.db.execute('SELECT * FROM users WHERE username = "%s"' %
                       username)  # sql query to fetch dat
    results = cur.fetchall()  # store all results
    g.db.close()  # close database connection
    return results  # returning result. end of get user detail function


def get_balance(accountNum):
    g.db = connect_db()  # g object call connect function
    cur = g.db.execute(
        'SELECT Balance FROM transactions WHERE transacitonID = (SELECT transacitonID FROM transactions WHERE accountNum = %s ORDER BY transacitonID DESC)' % accountNum)
    result = cur.fetchone()[0]  # store all results
    g.db.close()  # close databse connection
    return result  # returning result. end of get user detail function


def create_new_account(userid, type):
    g.db = connect_db()  # g object call connect database function
    cur = g.db.execute(  # sql query to fetch data
        'SELECT MAX(accountNum) FROM accounts WHERE userid = %s AND type = "%s"' % (userid, type))
    num = cur.fetchone()[0]  # store  the account type
    accountNum = num + 1
    cur = g.db.cursor()
    cur.execute(  # sql query to fetch data
        'INSERT INTO accounts (userid, accountNum, type) VALUES ( %s, %s, "%s" )' % (userid, accountNum, type))
    cur.execute(  # sql query to fetch data
        'INSERT INTO transactions ( accountNum, Balance) VALUES ( %s, 0 )' % accountNum)
    g.db.commit()
    g.db.close()  # close database connection


def to_transfer(from_num, to_num, amount, description):
    now = date.today()
    from_num = int(from_num)
    to_num = int(to_num)
    amount = int(amount)
    ob = get_balance(from_num) - amount
    nb = get_balance(to_num) + amount

    g.db = connect_db()  # g object call connect database function

    cur = g.db.cursor()
    cur.execute(  # sql query to fetch data
        'INSERT INTO transactions (accountNum, Date, TransactionDescription, Action, Amount, Balance) VALUES ( %s, "%s", "%s", "transfer", %s, %s )' % (
            from_num, now, description, amount, ob))

    cur.execute(  # sql query to fetch data
        'INSERT INTO transactions (accountNum, Date, TransactionDescription, Action, Amount, Balance) VALUES ( %s, "%s", "%s", "transfer", %s, %s )' % (
            to_num, now, description, amount, nb))

    g.db.commit()
    g.db.close()  # close database connection


if __name__ == "__main__":  # main
    app.run()
