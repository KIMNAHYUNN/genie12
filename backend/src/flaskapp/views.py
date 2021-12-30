from flask import request, g, Response, jsonify, render_template
from flaskapp import app
from flaskapp.db_utils import *
from flaskapp.vision import *
import os

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
    return render_template('luck.html')

@app.route('/card')
def route_card():
    return render_template('card.html')

@app.route('/result')
def route_result():
    tarot_id = "TA04"
    emotion_id = "0"
    intention_cd = "1"
    try:
        save_user_info(tarot_id, emotion_id, intention_cd)
    except:
        return Response(status=409)
    try:
        data = get_data()
    except:
        return Response(status=409)
    fortune_desc = data['fortune_desc']
    tarot_nm = data['tarot_nm']
    file_name = data['image_path']
    file_path = os.path.join("../static/image/", file_name)
    # return jsonify({
    #     "fortune_desc" : fortune_desc,
    #     "tarot_nm" : tarot_nm,
    #     "file_name" : file_name
    # })
    return render_template('result.html', fortune_desc=fortune_desc, tarot_nm=tarot_nm, file_path=file_path)

@app.route('/review')
def route_review():
    return render_template('review.html')

@app.route('/exit')
def route_exit():
    return render_template('exit.html')

@app.route('/detect_emotion')
def route_detect_emotion():
    val = gen_frames()

    return render_template('luck.html')


# @app.route('/detect_intention')
#
# @app.route('/detect_tarot_id')