from flask import Flask,g
import sqlite3

DATABASE = 'example.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/student/<key>')
def get_expreesion_duration(key):
    querys = query_db('select * from record where key= ?', [key])
    print(querys)

    return str(querys)

@app.route('/classroom')
def classroom():
    query_db("select")

    return 'index'


if __name__ == '__main__':
    app.run()

