#############################################################
#############################################################

### genietarot.py: ���� �ν�/��ȭ/���� �ռ�, �亯 �м�

#############################################################
#############################################################

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

KWSID = ['�Ⱑ����', '���Ͼ�', 'ģ����', '�ڱ��']

global text	# save dss_answer
text = ""

#def main():
def voiceTalk():
	"""���� �ν�/��ȭ/���� �ռ�"""

	global text

	# ���Ⱑ���ϡ� ��ȭ�� ���񽺸� ȣ��
	recog=kws.test(KWSID[0])

	if recog == 200:
		print('KWS Dectected ...\n')
		dss_answer = dss.queryByVoice()	# query by voice
		text = dss_answer

		tts_result = tts.getText2VoiceStream(dss_answer, "result_mesg.wav")

		if dss_answer == '':
			print('������ ������ �����ϴ�.\n\n\n')
		elif tts_result == 500:
			print("TTS ���� �����Դϴ�.\n\n\n")
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
	"""
	� �ǵ� ���� ���������� �����ϱ⡯ ��ư�� ������ get ��û ���ƿ�
	�������� ���, ������, ������� �� ������ � �ǵ��� json dictioary �������� return
	"""
	voiceTalk()
	if text == "������ ��� ���帱�Կ�.":
		return jsonify({'fortuneType': '������ �'})
	elif text == "������� ���帱�Կ�.":
		return jsonify({'fortuneType': '�����'})
	elif text == "�������� ���帱�Կ�.":
		return jsonify({'fortuneType': '������'})
	else:	
		return fortuneType()
    
if __name__ == '__main__':
   	#app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    app.run(host='0.0.0.0', port=5000)
	
# file end