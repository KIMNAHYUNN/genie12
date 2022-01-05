#############################################################
#############################################################

### views.py: Flask 웹 서버 구동과 관련된 함수들

#############################################################
#############################################################

from flask import request, g, Response, render_template, redirect, url_for
from flask import Flask, jsonify
#from flask import flash

from flaskapp import app
from flaskapp.db_utils import *
#from flaskapp.vision import *  # 구 버전
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

"""Flask의 route 데코레이터로 엔드포인트 등록 ("/")"""
@app.route('/')
def route_main(): # 엔드포인트 함수
    return render_template('index.html')

"""지니의 타로램프 - 시작 페이지"""
@app.route('/start')
def route_start():
    return render_template('start.html')

"""지니의 타로램프 - 운세 의도 페이지"""
@app.route('/luck')
def route_luck():
    #intention_nm = "오늘의 운세"
    #save_intention_nm(intention_nm)
    return render_template('luck.html')

"""지니의 타로램프 - 카드 뽑기 페이지"""
@app.route('/card')
def route_card():
    """카드 번호를 랜덤으로 생성, save_tarot_id 함수를 이용해서 db에 저장"""
    card_num = randint(0, 22)   # 카드 번호를 랜덤으로 생성
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

"""지니의 타로램프 - 운세 결과 페이지"""
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

"""지니의 타로램프 - 리뷰 페이지"""
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

"""사용자의 감정 데이터를 요청 및 저장"""
@app.route('/detect_emotion')
def route_detect_emotion():
    # vision_server에 감정의 긍정, 부정 여부 request
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

"""운세 의도 데이터를 요청 및 저장"""
@app.route('/detect_intention')
def route_detect_intention():
    # 기가지니 서버에 운세 의도 request
    params = {'key': 'value'}
    response = requests.get('http://172.30.1.43:5000/fortuneType', params=params)
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

"""운세 결과 데이터를 요청 및 저장"""
@app.route('/detect_result', methods=['POST'])
def route_detect_result():
    # freview.js에서 ajax로 보내준 별점 정보를 받아옴
    star = request.form['star']

    # DB에 저장
    save_tarot_result(star)
    return star

#############################################################
#############################################################

# file end