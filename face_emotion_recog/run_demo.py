from pathlib import Path 
    
import cv2 as cv

from emotion_recog import load_fer_model, inference

# Fact detection 모델 위치
detect_model_path = "./haarcascades_model/haarcascade_frontalface_default.xml"

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
               font_scale, color, thickness, line_type)

def main():
    # 얼굴 감지 모델, 감정 분류 모델 불러오기
    detect_model = cv.CascadeClassifier(detect_model_path)
    fer_model = load_fer_model(Path("./models/211231-100640-0.5086-bs_256_lr_0.001_mom_0.99_eps_0.001/"))

    cap = cv.VideoCapture(0) # 웹 캠 불러오기
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    cv.namedWindow("Demo") # 화면에 웹 캠 창 띄우기
    while True:
        # 웹 캠에서 이미지 읽기
        ret, bgr_img = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        gray_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2GRAY) # 얼굴 감정 분석용
        rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB) # 출력용
        
        # 얼굴 감지
        scale_factor = 1.3
        min_neighbors = 5
        faces = detect_model.detectMultiScale(gray_img, scale_factor, min_neighbors)
        for face_coords in faces:
            # (x1, y1): 얼굴 좌상단 좌표, (x2, y2) 얼굴 우하단 좌표
            x, y, h, w = face_coords
            x1, x2, y1, y2 = x, x+w, y, y+h 
            
            # 얼굴 이미지를 감정 분류 모델에 넣을 수 있도록 크기 변환
            gray_face = gray_img[y1:y2, x1:x2]
            gray_face = cv.resize(gray_face, FER_MODEL_INPUT_SHAPE)

            # 감정 분류
            emotion, prob, is_pos_emo = inference(fer_model, gray_face)
            
            # 얼굴 부분에 테두리 및 감정 표시
            color = emotion_to_color[emotion]
            draw_bounding_box(face_coords, rgb_img, color)
            draw_text(face_coords, rgb_img, f"{emotion}", color)
        
        # 윈도우에 이미지 출력
        updated_bgr_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2BGR)
        cv.imshow('Demo', updated_bgr_img)
        if cv.waitKey(1) == ord('q'): 
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
