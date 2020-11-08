from flask import Flask,g
import sqlite3
import json
import datetime

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
    return_data = {
        'happy': 0,
        'neutral': 0,
        'sleepy': 0
    }
    querys = query_db('select * from record where key= ?', [key])
    before_time = datetime.datetime.strptime(querys[0][3], "%Y-%m-%d %H:%M:%S")
    print(before_time)
    # query = (key:char(6), expression: text, eye_dir: text, time: datatime) - tuple
    for query in querys[1:]:
        current_time = datetime.datetime.strptime(query[3], "%Y-%m-%d %H:%M:%S")
        duration = (current_time-before_time).total_seconds()
        expression = query[1]
        return_data[expression] += duration
    return json.dumps(return_data )

@app.route('/classroom')
def classroom():
    # query_db return value : tuple
    keys = [i[0] for i in query_db('select distinct key from record')]
    ret = []
    for key in keys:
        data_form = {}
        data_form['key'] = key 
        data_form['exp_duration'] = json.loads(get_expreesion_duration(key))
        ret.append(data_form)
    return json.dumps(ret)

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0')


