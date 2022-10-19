
from naoqi import ALProxy
import time
import os

robot_IP = "192.168.0.108"
tts = audio = record = aup = None 



def record_NAO(robot_IP, robot_PORT=9559):
	global tts, audio, record, aup 
	# ----------> Connect to robot <----------
	tts = ALProxy("ALTextToSpeech", robot_IP, robot_PORT)
	audio = ALProxy("ALAudioDevice", robot_IP, robot_PORT)
	record = ALProxy("ALAudioRecorder", robot_IP, robot_PORT)
	aup = ALProxy("ALAudioPlayer", robot_IP, robot_PORT)
	memProxy = ALProxy("ALMemory",robot_IP, robot_PORT)
	# ----------> recording <----------
	print("start recording...")
	tts.say("start recording...")
	record_path = '/home/nao/record.wav'
	record.startMicrophonesRecording(record_path, 'wav', 16000, (1,1,1,1))
	time.sleep(3)
	record.stopMicrophonesRecording()
	print ('record over')
	tts.say("record over")

	cmd = 'scp nao@192.168.0.108:/home/nao/record.wav C:/Users/abdul/Desktop/Nao Robot/nao_test/Nao-Medical-Assistant'
	os.system(cmd)

record_NAO(robot_IP, robot_PORT=9559)