#############################################################
#############################################################

### vision_server.py: OpenCV를 활용하여 얼굴을 감지하고,
###                   학습된 PyTorch 모델을 불러와 감정을 분류
###                   별개의 flask 서버로 웹 서버와 통신

#############################################################
#############################################################

### http requests
import requests

### flask
from flask import Flask, render_template, Response, jsonify

from pathlib import Path

import numpy as np
import cv2 as cv
import os

from emotion_recog import load_fer_model, inference

#############################################################
#############################################################

# Fact detection 모델 위치
dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
detect_model_path = dir + "./haarcascades_model/haarcascade_frontalface_default.xml"

# 얼굴 부분에 칠할 박스의 색깔
emotion_to_color = {
    "angry":    [255,   0,   0], # Red
    "disgust":  [  0, 255,   0], # Green
    "fear":     [128,   0, 128], # Purple
    "happy":    [255, 165,   0], # Orange
    "neutral":  [128,   0,   0], # Brown
    "sad":      [  0,   0, 128], # Blue
    "surprise": [255, 255,   0]  # Yellow
}
FER_MODEL_INPUT_SHAPE = (48, 48)

def draw_bounding_box(coords, img, color):
    """얼굴 부분에 박스 그리기"""
    thickness = 2
    x, y, w, h = coords
    cv.rectangle(img, (x, y), (x + w, y + h), color, thickness) 

def draw_text(coords, img, text, color):
    """얼굴 박스 옆에 감정 글씨 넣기"""
    x, y, h, w = coords
    org = (x, y-10) # Bottom left position of the string
    font_scale = 1
    thickness = 2
    line_type = cv.LINE_AA

    cv.putText(img, text, org, cv.FONT_HERSHEY_SIMPLEX,
               font_scale, color, thickness, cv.LINE_AA)

#############################################################
#############################################################

app = Flask(__name__)

# emotion data
global value_emo 
value_emo = None

#############################################################

#def main():
def gen_frames():
    # 얼굴 감지 모델, 감정 분류 모델 불러오기
    detect_model = cv.CascadeClassifier(detect_model_path)
    path = dir + "./models/211231-100640-0.5086-bs_256_lr_0.001_mom_0.99_eps_0.001/"
    fer_model = load_fer_model(Path(path))

    # 웹캠
    cap = cv.VideoCapture(0) # Device index is 0
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    cv.namedWindow("Demo") # 웹캠 띄우기

    while True:
        # Capture frame-by-frame
        # 웹캠에서 이미지 읽기
        ret, bgr_img = cap.read()
        
        # If frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        gray_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2GRAY) # 얼굴 감정 분석용
        rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB) # 출력용
        
        # 사진에서 얼굴이 어디에 위치했는지 감지
        scale_factor = 1.3      # 큰 얼굴, 작은 얼굴을 모두 감지
        min_neighbors = 5       # 모델의 정확도를 높임
        faces = detect_model.detectMultiScale(gray_img, scale_factor, min_neighbors)

        # 한 화면에 얼굴이 여러 개 있을 경우
        for face_coords in faces:
            # (x1, y1): 얼굴 좌상단 좌표, (x2, y2) 얼굴 우하단 좌표
            x, y, h, w = face_coords
            x1, x2, y1, y2 = x, x+w, y, y+h
            
            # 얼굴 이미지를 감정 분류 모델에 넣을 수 있도록 크기 변환
            # to (48, 48)
            gray_face = gray_img[y1:y2, x1:x2]
            gray_face = cv.resize(gray_face, FER_MODEL_INPUT_SHAPE)

            # 감정 분류
            emotion, prob, is_pos_emo = inference(fer_model, gray_face)
            
            # save emotion data in global value 
            global value_emo
            value_emo = is_pos_emo
            #print(value_emo)

            # 얼굴 부분에 테두리 및 감정 표시
            color = emotion_to_color[emotion]
            draw_bounding_box(face_coords, rgb_img, color)
            draw_text(face_coords, rgb_img, f"{emotion}", color)

        # 윈도우에 이미지 출력        
        updated_bgr_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2BGR)
        cv.imshow('Demo', updated_bgr_img)

        if cv.waitKey(1) == ord('o'): 
            value_emo = is_pos_emo
            print("is_pos_emo: " + str(is_pos_emo))
        
        # how to quit
        if cv.waitKey(1) == ord('q'): 
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

#############################################################
#############################################################

'''
@app.route('/')
def Hello():
    return 'Hello World!'
'''

### localhost:1070
### 얼굴 감지하는 창을 유지
@app.route('/')
def gen():
    return gen_frames()

### localhost:1070/emotion
@app.route('/emotion')
def returnEmoton():
    """
    웹 서버에서 감정 상태에 대한 데이터 요청이 들어왔을 시,
    is_pos_emo를 json dictionary 형태로 반환
    """
    print(value_emo)
    return jsonify({'is_pos_emo' : value_emo})

# flask server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='1070', debug=True)
    #main()

# file end