from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

global value_fortune
value_fortune = None

@app.route('/')
def route_home():
    return render_template('flask_button.html')

'''
@app.route('/call_fortune')
def wantWhichFortune():
    params = {'key': 'value'}
    response = requests.get('http://127.0.0.1:3000/giveWhichFortune', params=params)
    response_data = response.json()

    global value_fortune
    value_fortune = response_data['fortune']
    print("I got it!: " + value_fortune)
    return render_template('test.html')
'''

@app.route('/call_v2t')
def wantV2T():
    params = {'key': 'value'}
    response = requests.get('http://192.168.219.113:5000/v2t', params=params)
    #response = requests.get('http://127.0.0.1:5000/emotion')
    #print(response.json())
    #return(response.json())
    response_data = response.json()
    print("I got it!: " + response_data['v2t'])
    return 'yes!'

##############################################################################
# 어떤 운세?: 
# 오늘의 운세(fortune_today), 성취운(fortune_success), 금전운(fortune_money) 
# {'fortune type': text}
app.route('/call_fortuneType')
def wantFortuneType():
    params = {'key': 'value'}
    response = requests.get('http://192.168.219.113:5000/fortuneType', params=params)
    response_data = response.json()
    print("I got it! fortune type: " + response_data['fortyneType'])
    return 'fortune type ok!'

# 몇 번 카드?: 
# 1~22 
# {'fortune type': text}
app.route('/call_pickOneCard')
def wantPickOneCard():
    params = {'key': 'value'}
    response = requests.get('http://192.168.219.113:5000/pickOneCard', params=params)
    response_data = response.json()
    print("I got it! prickOneCard: " + response_data['pickOnCard'])
    return 'fortune type ok!'

if __name__ == '__main__':
    #app.run(debug = True)
     app.run(host='0.0.0.0', port=2007, threaded=True)