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

# @app.route('/luck')
# def route_luck():
#     intention_nm = "오늘의 운세"
#     save_intention_nm(intention_nm)
#     return render_template('luck.html')

@app.route('/card')
def route_card():
    tarot_id = "TA05"
    save_tarot_id(tarot_id)
    return render_template('card.html')

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
    intention_nm = "오늘의 운세"
    save_intention_nm(intention_nm)
    return render_template('luck.html')


# @app.route('/detect_intention')
#
# @app.route('/detect_tarot_id')