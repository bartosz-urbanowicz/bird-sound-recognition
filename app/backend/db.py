import sqlite3
from flask import g

DATABASE = "database.db"

def init_db():
    connection = sqlite3.connect(DATABASE)
    with open('schema.sql') as f:
        connection.executescript(f.read())
    cur = connection.cursor()
    cur.execute("INSERT INTO observations (species, location) VALUES (?, ?)",
                ("Parus major", "1,1")
                )
    cur.execute("INSERT INTO users (username, email) VALUES (?, ?)",
                ("admin", "admin@mail.com")
                )
    connection.commit()
    connection.close()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    db = get_db()
    cur = get_db().execute(query, args)
    db.commit()
    success = cur.rowcount > 0
    cur.close()
    return success

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_connection)