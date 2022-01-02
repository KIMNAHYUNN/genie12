#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function # must be at the top

import MicrophoneStream as MS
import ex1_kwstest as kws
import ex4_getText2VoiceStream as tts
import ex6_queryVoice as dss
import time

from flask import Flask, render_template, Response, jsonify
import requests

app = Flask(__name__)

KWSID = ['기가지니', '지니야', '친구야', '자기야']

global text
text = ""

#def main():
def mainee():
	global text
	#Example8 KWS+STT+DSS
	recog=kws.test(KWSID[0])

	if recog == 200:
		print('KWS Dectected ...\n')
		dss_answer = dss.queryByVoice()
		text = dss_answer

		tts_result = tts.getText2VoiceStream(dss_answer, "result_mesg.wav")

		if dss_answer == '':
			print('질의한 내용이 없습니다.\n\n\n')
		elif tts_result == 500:
			print("TTS 동작 에러입니다.\n\n\n")
		else:
			MS.play_file("result_mesg.wav")			
		    #time.sleep(2)
	else:
		print('KWS Not Dectected ...')

############################################################
############################################################
# Flask

@app.route('/')
def hello_world():
    return 'genie tarot - main'
    
@app.route('/fortuneType')
def fortuneType():
	text = mainee()
	if text == "오늘의 운세를 봐드릴게요.":
		return jsonify({'fortuneType': '오늘의 운세'})
	elif text == "성취운을 봐드릴게요.":
		return jsonify({'fortuneType': '성취운'})
	elif text == "금전운을 봐드릴게요.":
		return jsonify({'fortuneType': '금전운'})
	else:
		return jsonify({'fortuneType': 'oops'})
    
if __name__ == '__main__':
   	#app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    app.run(host='0.0.0.0', port=5000)
	
	
