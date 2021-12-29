from flask import request, g, Response, jsonify, render_template
from flaskapp import app
from flaskapp.db_utils import *

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
    return render_template('result.html')

@app.route('/review')
def route_review():
    return render_template('review.html')

@app.route('/exit')
def route_exit():
    return render_template('exit.html')

@app.route('/tarot')
def route_tarot():
    tarot_id = "TA04"
    emotion_id = "0"
    try:
        save_user_info(tarot_id, emotion_id)
    except:
        return Response(status=409)
    return "Success"

    # tarot_name = get_tarot_mas(tarot_id)
    #
    # return jsonify({
    #     'tarot_name':tarot_name
    # })
