220103 12:28 수정 사항 (readme 수정 중)

# backend
import 관련 오류들을 해결하기 위해 app 형태로 실행되던 vision.py 파일 대신 vision_server.py를 사용하도록 하였습니다.
(내용은 거의 동일) 

cmd를 따로 열어 vision_server.py 를 실행하면 localhost:1070 에서 실행됩니다.
시연 시 반드시 1060과 1070에서 모두 서버가 돌아가도록 켜줘야 합니다.

# 라즈베리 파이 참고 사항

genietarot.py 를 예제 파일들이 들어있는 python3 폴더에 넣어줍니다.

이때, KT API Link에 등록한 구문 목록을 인식하려면 동일 폴더에 들어있는 user_auth.py 에 콘솔창에서 열람할 수 있는 ID/KEY/SECRET을 입력해주어야 합니다.
콘솔창에서는 KEY/ID/SECRET 순서로 뜨니 입력 시 주의하세요.

라즈베리 파이에서는 서버 실행 시 python3 파일명 으로 실행해주어야 합니다.
genietarot.py 는 localhost:5000 에서 실행됩니다.
