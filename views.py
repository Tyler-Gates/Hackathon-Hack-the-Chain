"""
Routes and views for the flask application.
"""

from datetime import datetime
from functools import wraps
from flask import render_template, request, url_for, redirect, Flask, session, flash, g
from FlaskWebProject1 import app
import sqlite3

with sqlite3.connect("user.db") as connection:
    c = connection.cursor()
    c.execute("DROP TABLE posts")
    c.execute("CREATE TABLE posts(user TEXT, passw TEXT, seed TEXT)")
    c.execute('INSERT INTO posts VALUES("Grant", "Berns", "aslkdjfn6542lkj2n3asj232Kajs")')
    c.execute('INSERT INTO posts VALUES("Harry", "Styles", "yin6nUhaE822hAnsdk34jkD")')
    c.execute('INSERT INTO posts VALUES("Howard", "Wallowitz", "L43kIlB8dHo9hqurR3s")')

app.secret_key = "my precious"
app.database = "user.db"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap



@app.route('/')
@app.route('/index')
def index():
    """Renders the start page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
    )

@app.route('/shirt')
def shirt():
    """Renders the shirt page."""
    return render_template(
        'shirt.html',
        title='Shirt',
        year=datetime.now().year,
    )

@app.route('/Hshirt')
@login_required
def Hshirt():
    """Renders the shirt page."""
    return render_template(
        'Hshirt.html',
        title='Shirt',
        year=datetime.now().year,
    )

@app.route('/sticker')
def sticker():
    """Renders the shirt page."""
    return render_template(
        'sticker.html',
        title='Sticker',
        year=datetime.now().year,
    )

@app.route('/Hsticker')
@login_required
def Hsticker():
    """Renders the shirt page."""
    return render_template(
        'Hsticker.html',
        title='Sticker',
        year=datetime.now().year,
    )

@app.route('/home')
@login_required
def home():
    """Renders the home (logged in) page."""
    return render_template(
        'home.html',
        title='Home',
        year=datetime.now().year,
    )

@app.route('/homePage')
@login_required
def homePage():
    """Renders the home (logged in) page."""
    return render_template(
        'homePage.html',
        title='Home',
        year=datetime.now().year,
    )

@app.route('/Hmerch')
@login_required
def Hmerch():
    """Renders the contact page."""
    return render_template(
        'Hmerch.html',
        title='Merch',
        year=datetime.now().year,
        message='MLH SWAG'
    )

@app.route('/merch')
def merch():
    """Renders the contact page."""
    return render_template(
        'merch.html',
        title='Merch',
        year=datetime.now().year,
        message='MLH SWAG'
    )

@app.route('/account')
@login_required
def account():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(user=row[0], passw=row[1], seed=row[2]) for row in cur.fetchall()]
    g.db.close()
    """Renders the account page."""
    return render_template(
        'account.html',
        title='Admin',
        year=datetime.now().year,
        message='Admin', posts=posts
    )

@app.route('/Habout')
@login_required
def Habout():
    """Renders the about page."""
    return render_template(
        'Habout.html',
        title='About',
        year=datetime.now().year,
        message='MLH merch is stored here!'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='MLH merch is stored here!'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('homePage'))
    return render_template(
        'login.html', error=error, year=datetime.now().year,
    )

@app.route('/create', methods=['GET', 'POST'])
def create():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('homePage'))
    return render_template(
        'create.html', error=error, year=datetime.now().year,
    )

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('index'))


def connect_db():
    return sqlite3.connect(app.database)