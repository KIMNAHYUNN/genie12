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

# haungul
# app.config['JSON_AS_ASCII'] = False

#############################################################
#############################################################

@app.teardown_appcontext
def close_db(e=None):
    # executed when application context is gone
    db = g.pop('db', None)
    if db is not None:
        db.close()

#############################################################
#############################################################

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
    # 카드 번호를 랜덤으로 생성
    card_num = randint(0, 22)
    if card_num < 10:
        tarot_id = "TA0" + str(card_num)
    else:
        tarot_id = "TA" + str(card_num)
    
    # db에 저장
    save_tarot_id(tarot_id)
    
    # 카드의 이미지가 있는 경로를 만듦
    file_path = os.path.join('../static/image/', tarot_id)
    file_path += '.jpg'
    
    # console print
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

    # 타로 결과를 보여주기 위해 필요한 정보들을 DB에서 가져옴
    fortune_desc = data['fortune_desc']
    INTENTION_NM = data['intention_nm']
    file_name = data['image_path']
    file_path = os.path.join("../static/image/", file_name)
    emotion_id = data['emotion_id']

    # console print
    print(emotion_id)

    return render_template('result.html', intention_nm=INTENTION_NM,fortune_desc=fortune_desc, file_path=file_path, emotion_id=emotion_id)

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

    # console print
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
    # console print
    print("I got it! fortune type: " + intention_nm)

    # 받은 intention 데이터에 따라 다른 값을 DB에 저장
    if intention_nm == 'today':
        save_intention_nm('오늘의 운세')
    elif intention_nm == 'success':
        save_intention_nm('성취운')
    elif intention_nm == 'money':
        save_intention_nm('금전운')
    else:
        save_intention_nm('오늘의 운세')
    
    return(route_luck())

#############################################################
#############################################################

@app.route('/detect_result', methods=['POST'])
def route_detect_result():
    # freview.js에서 ajax로 보내준 별점 정보를 받아옴
    star = request.form['star']

    # DB에 저장
    save_tarot_result(star)
    return star

#############################################################
#############################################################