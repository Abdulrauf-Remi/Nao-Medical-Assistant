
# Network settings of the robot
NAO_IP = "192.168.0.108"         # the current IP address of the NAO
NAO_port = 9559

from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", NAO_IP, 9559)
tts.say("")