# 데모 실행 방법
* face_emotion_recog 폴더에서 쉬프트+마우스 오른쪽 버튼 동시에 눌러서 '여기에 PowerShell 창 열기' 클릭

* PowerShell 창이 열리면 다음과 같이 입력
```
face_emotion_recog> cmd
face_emotion_recog> python -m venv venv
face_emotion_recog> venv\Scripts\activate
(venv) face_emotion_recog> pip install -r requirements.txt
(venv) face_emotion_recog> python run_demo.py
```
* 안경을 벗으면 얼굴 인식이 더 잘됩니다
* 종료하려면 키보드에서 q  입력
* 가상 환경 나가려면 deactivate 입력
```
(venv) face_emotion_recog> deactivate
```

# 학습
1. https://www.kaggle.com/msambare/fer2013 에서 데이터셋을 다운로드
2. 압축을 풀고 'train' 폴더와 'test' 폴더를 'dataset' 폴더로 이동 