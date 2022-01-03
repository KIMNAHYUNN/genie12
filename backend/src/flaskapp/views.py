from flask import request, g, Response, render_template, redirect, url_for
from flask import Flask, jsonify
#from flask import flash

from flaskapp import app
from flaskapp.db_utils import *
#from flaskapp.vision import *
from flaskapp.voice import *

import os
import requests
from random import *

app.config['JSON_AS_ASCII'] = False

global resulttext
resulttext = ""

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
    #intention_nm = "오늘의 운세"
    #save_intention_nm(intention_nm)
    return render_template('luck.html')

@app.route('/card')
def route_card():
    tarot_id = "TA12"
    #card_num = 5
    #save_tarot_id(tarot_id)
    #return render_template('card.html', card_num=card_num)
    card_num = randint(0, 22)
    # if card_num < 10:
    #     tarot_id = "TA0" + str(card_num)
    # else:
    #     tarot_id = "TA" + str(card_num)
    save_tarot_id(tarot_id)
    file_path = os.path.join('../static/image/', tarot_id)
    file_path += '.jpg'
    
    print(file_path)
        
    return render_template('card.html', file_path=file_path)

#@app.route('/requestspeak')
def requestspeak():
    return redirect("http://172.30.1.31:5000/speak", code=302)

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
    INTENTION_NM = data['intention_nm']
    file_name = data['image_path']
    file_path = os.path.join("../static/image/", file_name)
    emotion_id = data['emotion_id']
    print(emotion_id)
    
    global resulttext
    resulttext = "["+ INTENTION_NM +"]<br>" + fortune_desc

    requestspeak()

    return render_template('result.html', intention_nm=INTENTION_NM,fortune_desc=fortune_desc, file_path=file_path, emotion_id=emotion_id)


@app.route('/answerspeak')
def answerspeak():
    global resulttext
    print(resulttext)
    return jsonify({'text': resulttext})

@app.route('/review')
def route_review():
    #tarot_result = 4
    #save_tarot_result(tarot_result)
    return render_template('review.html')

@app.route('/exit')
def route_exit():
    return render_template('exit.html')

#############################################################
#############################################################

'''
@app.route('/detect_emotion')
def route_detect_emotion():
    response_data = gen_frames()
    bool = response_data['emotions']
    if bool:
        save_emotion_id("EM01")
    else:
        save_emotion_id("EM00")
    return redirect(url_for('route_luck'))
'''

@app.route('/detect_emotion')
def route_detect_emotion():
    # request emotion data to vision_server
    params = {'key': 'value'}
    response = requests.get('http://127.0.0.1:1070/emotion', params=params)
    response_data = response.json()

    if response_data['is_pos_emo'] is True: 
        save_emotion_id("EM01") #happy
    else:
        save_emotion_id("EM00") #sad

    print("I got it! is_pos_emo: " + str(response_data['is_pos_emo']))
    #flash("is_pos_emo: " + str(response_data['is_pos_emo']))
    return(route_start())   # return to default page

#############################################################
#############################################################

@app.route('/detect_intention')
def route_detect_intention():
    # request emotion data to raspberry pi server for detecting intention
    params = {'key': 'value'}
    response = requests.get('http://172.30.1.31:5000/fortuneType', params=params)
    response_data = response.json()
    
    intention_nm = str(response_data['fortuneType'])
    print("I got it! fortune type: " + intention_nm)

    if intention_nm == 'today':
        save_intention_nm('오늘의 운세')
    elif intention_nm == 'success':
        save_intention_nm('성취운')
    elif intention_nm == 'money':
        save_intention_nm('금전운')
    else:
        save_intention_nm('오늘의 운세')
    
    return(route_luck())

@app.route('/detect_result', methods=['POST'])
def route_detect_result():
    star = request.form['star']
    save_tarot_result(star)
    return star

#############################################################
#############################################################

'''
@app.route('/detect_tarot_id')
def route_detect_card():
    params = {'key': 'value'}
    response = requests.get('http://192.168.219.113:5000/pickOneCard', params=params)
    response_data = response.json()

    print("I got it! prickOneCard: " + response_data['pickOnCard'])
    return 'fortune type ok!'
'''