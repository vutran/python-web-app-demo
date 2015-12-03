# import modules
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# db configs
DATABASE = './flaskr.db'
DEBUG = True
SECRET_KEY = 'this_is_a_super_secret_key'
USERNAME = 'root'
PASSWORD = 'root'

def init_db():
    # initializes the db
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    """
    Connects to the database and returns a Connection instance
    """
    return sqlite3.connect(app.config['DATABASE'])

# create the app
app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# create routes
@app.route("/")
def home():
    cursor = g.db.execute('select id, title, text, created_date from entries order by id desc')
    print(cursor.fetchall())
    return render_template('home.html', page_title="Home")

@app.route("/about/")
def about():
    return render_template('about.html', page_title="About")

@app.route("/contact/")
def contact():
    return render_template('contact.html', page_title="Contact")

# run the app if called directly
if __name__ == "__main__":
    # initialize the database
    init_db()
    # enable debug mode
    app.debug = True
    app.run(host='0.0.0.0')
