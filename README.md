220103 23:49 수정 사항

# backend
import 관련 오류들을 해결하기 위해 app 형태로 실행되던 vision.py 파일 대신 vision_server.py를 사용하도록 하였습니다.
(내용은 거의 동일) 

cmd를 따로 열어 vision_server.py 를 실행하면 localhost:1070 에서 실행됩니다.

시연 시 반드시 1060과 1070에서 모두 서버가 돌아가도록 켜줘야 합니다.

# 라즈베리 파이 참고 사항

### 1. genietarot.py 관련

genietarot.py 를 예제 파일들이 들어있는 python3 폴더에 넣어줍니다.

이때, KT API Link에 등록한 구문 목록을 인식하려면 동일 폴더에 들어있는 user_auth.py 에 콘솔창에서 열람할 수 있는 ID/KEY/SECRET을 입력해주어야 합니다.
콘솔창에서는 KEY/ID/SECRET 순서로 뜨니 입력 시 주의하세요.

구문 목록은 함께 공유해서 사용하고 있는 구글 타로카드 스프레드시트를 열람하거나, 콘솔창 담당 팀원에게 문의해주세요.

라즈베리 파이에서는 서버 실행 시 python3 파일명 으로 실행해주어야 합니다.
genietarot.py 는 localhost:5000 에서 실행됩니다.

### 2. 고정 IP 설정

~~backend용 기기와 라즈베리 파이가 동일 와이파이에 연결되어있는지 확인하고, 라즈베리 파이의 IP를 고정 IP로 변경해주세요.~~

~~고정 IP는 /etc/dhcpcd.conf 에서 변경하면 됩니다.~~

~~해당 파일이 존재하지 않는다면 dhcp 패키지를 먼저 설치해주세요.~~

```
sudo apt install dhcpcd5
```

~~그리고 /etc/dhcpcd.conf 파일 내에서는 다음 두 줄을 변경합니다.~~

```
static ip_address = 본인 IP 주소 (ifconfig)

static routers = 게이트웨이 주소 (맨 끝자리만 1)
```
### 3. 이미지 관련

라즈베리 파이의 이미지 파일이 손상되었을 경우, 화면이 나오지 않거나 부팅이 되지 않는 등의 문제가 일어납니다. 

이 경우에는 SD카드를 포맷하고 이미지 파일을 재설치하는 편이 가장 빠릅니다.

작동하지 않는 파일: amk_genieblock_v1.3.img (콘솔 다운로드)

작동하는 파일: kt_acp_rpi4__v3.4.img (노트북 탑재)

라즈베리 파이 이미저로 라즈베리 파이 측에서 제공하는 이미지 파일을 설치할 경우, easy_install을 사용할 수 없어 audio가 작동하지 않는 문제가 있습니다.

### 4. 초반 설치

```
sudo apt update

sudo apt-get install ufw
sudo ufw allow 22
sudo ufw allow 5000

sudo apt-get install libasound-dev
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev -y
sudo apt-get install python3-pyaudio
cd ~/ai-makers-kit/python/install/
sudo python3 -m easy_install ktkws-1.0.1-py3.5-linux-armv7l.egg
sudo pip3 install grpcio grpcio-tools
```
