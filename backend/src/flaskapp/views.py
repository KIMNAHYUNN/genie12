from flask import request, g, Response, jsonify, render_template, redirect, url_for
from flaskapp import app
from flaskapp.db_utils import *
from flaskapp.vision import *
import os
import random

@app.teardown_appcontext
def close_db(e=None):
    # executed when application context is gone
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def route_main():
    return render_template('index.html')

@app.route('/start')
def route_start():
    return render_template('start.html')

@app.route('/luck')
def route_luck():
    intention_nm = "오늘의 운세"
    save_intention_nm(intention_nm)
    return render_template('luck.html')

@app.route('/card')
def route_card():
    # tarot_id = "TA05"
    tarot_id = random.randrange(0, 22)
    if tarot_id < 10:
        tarot_id = 'TA' + '0' + str(tarot_id)
    else:
        tarot_id = 'TA' + str(tarot_id)
    save_tarot_id(tarot_id)
    file_path = os.path.join('../static/image/', tarot_id)
    file_path += '.jpg'
    print(file_path)
    return render_template('card.html', file_path=file_path)

@app.route('/result')
def route_result():
    try:
        save_user_info()
    except:
        return Response(status=403)
    try:
        data = get_data()
    except:
        return Response(status=409)
    fortune_desc = data['fortune_desc']
    file_name = data['image_path']
    file_path = os.path.join("../static/image/", file_name)
    return render_template('result.html', fortune_desc=fortune_desc, file_path=file_path)

@app.route('/review')
def route_review():
    tarot_result = 4
    save_tarot_result(tarot_result)
    return render_template('review.html')

@app.route('/exit')
def route_exit():
    return render_template('exit.html')

@app.route('/detect_emotion')
def route_detect_emotion():
    response_data = gen_frames()
    bool = response_data['emotion']
    if bool:
        save_emotion_id("EM01")
    else:
        save_emotion_id("EM00")
    return redirect(url_for('route_luck'))

@app.route('/call_v2t')
def wantV2T():
    params = {'key': 'value'}
    response = requests.get('http://192.168.219.113:5000/v2t', params=params)
    response_data = response.json()
    print("I got it!: " + response_data['v2t'])
    return 'yes!'

@app.route('/detect_intention')
def route_detect_intention():
    params = {'key': 'value'}
    response = requests.get('http://192.168.219.113:5000/fortuneType', params=params)
    response_data = response.json()
    print("I got it! fortune type: " + response_data['fortuneType'])
    return 'fortune type ok!'

@app.route('/detect_result', methods=['POST'])
def route_detect_result():
    star = request.form['star']
    save_tarot_result(star)
    return star