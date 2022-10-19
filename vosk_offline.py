import speak
# Network settings of the robot
NAO_IP = "192.168.0.108"         # the current IP address of the NAO
NAO_port = 9559

speakModule = speak.SpeakModule("speakModule", NAO_IP, NAO_port)

speakModule.say("Nkassenkasee")