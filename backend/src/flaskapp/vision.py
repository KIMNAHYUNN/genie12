### http requests
import requests

### flask
from flask import Flask, render_template, Response, jsonify

### opencv
from pathlib import Path

import numpy as np
import cv2 as cv
import os
from flaskapp.emotion_recog import load_fer_model, inference

#############################################################
#############################################################

dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
detect_model_path = dir + "./haarcascades_model/haarcascade_frontalface_default.xml"
emotion_to_color = {
    "angry": [255, 0, 0],  # Red
    "disgust": [0, 255, 0],  # Green
    "fear": [128, 0, 128],  # Purple
    "happy": [255, 165, 0],  # Orange
    "neutral": [128, 0, 0],  # Brown
    "sad": [0, 0, 128],  # Blue
    "surprise": [255, 255, 0]  # Yellow
}
FER_MODEL_INPUT_SHAPE = (48, 48)


def draw_bounding_box(coords, img, color):
    thickness = 2
    x, y, w, h = coords
    cv.rectangle(img, (x, y), (x + w, y + h), color, thickness)


def draw_text(coords, img, text, color):
    x, y, h, w = coords
    org = (x, y - 10)  # Bottom left position of the string
    font_scale = 1
    thickness = 2
    line_type = cv.LINE_AA

    cv.putText(img, text, org, cv.FONT_HERSHEY_SIMPLEX,
               font_scale, color, thickness, cv.LINE_AA)

# emotion data
global value_emo
value_emo = None


def gen_frames():
    detect_model = cv.CascadeClassifier(detect_model_path)
    path = dir + "./models/211231-100640-0.5086-bs_256_lr_0.001_mom_0.99_eps_0.001/"
    fer_model = load_fer_model(Path(path))

    cap = cv.VideoCapture(0)  # Device index is 0
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    cv.namedWindow("Demo")

    while True:
        # Capture frame-by-frame
        ret, bgr_img = cap.read()
        # If frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        gray_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2GRAY)  # For emotion recognition
        rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)  # For drawing

        scale_factor = 1.3
        min_neighbors = 5
        faces = detect_model.detectMultiScale(gray_img, scale_factor, min_neighbors)
        for face_coords in faces:
            x, y, h, w = face_coords
            x1, x2, y1, y2 = x, x + w, y, y + h

            gray_face = gray_img[y1:y2, x1:x2]
            gray_face = cv.resize(gray_face, FER_MODEL_INPUT_SHAPE)

            emotion, prob, is_pos_emo = inference(fer_model, gray_face)

            # save emotion data in global value
            global value_emo
            value_emo = is_pos_emo
            # print(value_emo)

            color = emotion_to_color[emotion]
            draw_bounding_box(face_coords, rgb_img, color)
            draw_text(face_coords, rgb_img, f"{emotion}", color)

        updated_bgr_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2BGR)
        cv.imshow('Demo', updated_bgr_img)

        '''
        if cv.waitKey(1) == ord('o'): 
            #URL = 'http://www.tistory.com'
            #response = requests.get(URL)
            #print(response.status_code)
            value_emo = emotion
            print(emotion)
        '''

        # how to quit
        if cv.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    print("Vision Emotion Capture Worked!: " + is_pos_emo)

    return {'emotion': is_pos_emo}

# file end