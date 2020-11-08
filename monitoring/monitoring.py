from flask import Flask,g
from db import DB
import json
import datetime

app = Flask(__name__)

@app.route('/student/<key>')
def get_expreesion_duration(key):
    db = DB()
    return_data = {
        'happy': 0,
        'neutral': 0,
        'sleepy': 0
    }
    querys = list(db.query(f"select * from record where s_id = '{key}'").get_points())
    # query = (key:char(6), expression: text, eye_dir: text, time: datatime) - tuple
    for query in querys:
        expression = query["expression"]
        duration = query["duration"]
        return_data[expression] += duration
    for k in return_data.keys():
        return_data[k] = round(return_data[k],2)
    return json.dumps(return_data)

@app.route('/classroom')
def classroom():
    db = DB()
    # query_db return value : tuple
    keys = [q['distinct'] for q in list(db.query('select distinct(s_id) from record').get_points())]
    ret = []
    for key in keys:
        data_form = {}
        data_form['key'] = key 
        data_form['exp_duration'] = json.loads(get_expreesion_duration(key))
        ret.append(data_form)
    return json.dumps(ret)

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', debug=False)