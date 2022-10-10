# Libraries
from naoqi import ALBroker, ALProxy
import time
import sys
# import zmq

# external Python files
import speak
import move
import speechReco
import soundDetect
import faceDetect
from speech_to_text import speech_to_text
# import googleSpeechReco
import dialog
import requests

# Naoqi modules
speakModule = None
moveModule = None
speechRecoModule = None
vocabulary = "yes;no;okay"     # key words for NAOQi speech recognition
soundDetectModule = None
faceDetectModule = None

# Network settings of the robot
NAO_IP = "192.168.0.100"         # the current IP address of the NAO
NAO_port = 9559

# This is the robot control. It also interacts with the user interface GUI (userInterface.py)
def main():

    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,          # parent broker IP
       NAO_port)        # parent broker port
       
    # here we comment some modules. E.g., we use Google speech-to-text API rather than internal NAOQi speech recognition (speechRecoModule)
    global speakModule
    speakModule = speak.SpeakModule("speakModule", NAO_IP, NAO_port)
    global moveModule
    moveModule = move.MoveModule("moveModule", NAO_IP, NAO_port)
    # global speechRecoModule
    # speechRecoModule = speechReco.SpeechRecoModule("speechRecoModule", vocabulary)
    # global soundDetectModule					
    # soundDetectModule = soundDetect.SoundDetectModule("soundDetectModule")
    global faceDetectModule					
    faceDetectModule = faceDetect.FaceDetectModule("faceDetectModule")
    # global speechRecogniser
    # speechRecogniser = googleSpeechReco.SpeechRecogniser()
    global dialog
    dialog = dialog.Dialog(moveModule)
    
    
    # set face tracking (only work when NAO Auto-life enabled)
    faceProxy = ALProxy("ALFaceDetection")
    faceProxy.enableTracking(True)
    
    
    # LOOP
    try:

        while True:
            human_input = speech_to_text()     # reveive transcript that contains keyword
            if "dance" in human_input:
                speakModule.say(dialog.answer(human_input))
            elif "sit down" in human_input:
                speakModule.say(dialog.answer(human_input))
            elif "stand up" in human_input:
                speakModule.say(dialog.answer(human_input))

            resp = requests.post("http://localhost:5000/predict", data=human_input)
            
            print(resp.text)
            speakModule.say(str(resp.text))  # react to the transcript 
                             
 	    
    except KeyboardInterrupt:
    	
        print ("Interrupted by user, shutting down")
        myBroker.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()