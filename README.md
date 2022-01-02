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

구문 목록은 함께 공유해서 사용하고 있는 구글 타로카드 스프레드시트를 열람하거나, 콘솔창 담당 팀원에게 문의해주세요.

라즈베리 파이에서는 서버 실행 시 python3 파일명 으로 실행해주어야 합니다.
genietarot.py 는 localhost:5000 에서 실행됩니다.

backend용 기기와 라즈베리 파이가 동일 와이파이에 연결되어있는지 확인하고, 라즈베리 파이의 IP를 고정 IP로 변경해주세요. (해당 IP는 view.py에서 열람 가능합니다.)

고정 IP는 /etc/dhcpcd.conf 에서 변경하면 됩니다.
해당 파일이 존재하지 않는다면 dhcp 패키지를 먼저 설치해주세요.

sudo apt install dhcpcd

/etc/dhcpcd.conf 파일 내에서는 다음 두 줄을 변경합니다.
static ip_address = 본인 IP 주소 (ifconfig)
static routers = 게이트웨이 주소 (맨 끝자리만 1)
