# Libraries
from naoqi import ALBroker, ALProxy
import time
import sys


# external Python files
import speak
import move
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
NAO_IP = "192.168.0.104"         # the current IP address of the NAO
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

    fever_follow = "Do you have any other symptoms such as abdominal pain, rashes or faint pink spots, usually on your chest or stomach, cough, diarrhea or constipation"
    typhoid_true = "Then you have typhoid fever"
    
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
            speakModule.say(str(resp.text)) # react to the transcript 
            if "fever" in str(resp.text):
                print(fever_follow)
                time.sleep(1)
                speakModule.say(fever_follow)
                feverfans = speech_to_text()
                if "yes" in feverfans:
                    print(typhoid_true)
                    time.sleep(1)
                    speakModule.say(typhoid_true)
                    time.sleep(2)
                    speakModule.say("Typhoid fever is a bacterial infection that can spread throughout the body, affecting many organs. Without prompt treatment, it can cause serious complications and can be fatal.")
                    sym_dur = "how long have you been exprencing those symptoms"
                    print(sym_dur)
                    time.sleep(2)
                    speakModule.say(sym_dur)
                    sym_dur_res = speech_to_text()
                    ty_dur = requests.post("http://localhost:5000/predict", data=sym_dur_res)
                    if "early stage" in str(ty_dur.text):
                        print("the pharmacist will provide you with antibiotics which may include Ciprofloxacin, Ceftriaxone, Azithromycin or Carbapenems")
                        speakModule.say("the pharmacist will provide you with antibiotics which may include Ciprofloxacin, Ceftriaxone, Azithromycin or Carbapenems.")
                        time.sleep(2)
                        speakModule.say("Your symptoms should begin to improve within 2 to 3 days of taking antibiotics. But it's very important you finish the course\
                             to ensure the bacteria are completely removed from your body.")
                        speakModule.say("Please take note of the follow preventions to avoid future typhoid infection")
                        typ_ques = "preventions for typhoid"
                        resp = requests.post("http://localhost:5000/predict", data=typ_ques)
                        print(resp.text)
                        speakModule.say(str(resp.text))
                        time.sleep(2)
                        speakModule.say("If you are unsure, its safest to drink bottled water or boil water before drinking")
                    else:
                        print("I will suggest you go to the laboratory for your samples be tested to determine which strain\
                            you're infected with, so you can be treated with an appropriate antibiotic")
                        speakModule.say("I will suggest you go to the laboratory for your samples be tested to determine which strain\
                            you're infected with, so you can be treated with an appropriate antibiotic")
                        time.sleep(1)
                        speakModule.say("Please, doctor Mensah will take over after your samples have been tested")
                else:
                    speakModule.say("A fever is a temporary rise in body temperature. It's one part of an overall response from the body's immune system. A fever is usually caused by an infection.")
                    fever_ques = "medicine for fever"
                    resp = requests.post("http://localhost:5000/predict", data=fever_ques)
                    print(resp.text)
                    speakModule.say(str(resp.text))

                    fever_ques = "What to eat to avoid getting fever"
                    resp = requests.post("http://localhost:5000/predict", data=fever_ques)
                    print(resp.text)
                    speakModule.say(str(resp.text))

                    fever_ques = "any preventions for fever"
                    resp = requests.post("http://localhost:5000/predict", data=fever_ques)
                    print(resp.text)
                    speakModule.say(str(resp.text))
                    time.sleep(2)
                    speakModule.say("Please go to the pharmacy for your medication")

 	    
    except KeyboardInterrupt:
    	
        print ("Interrupted by user, shutting down")
        myBroker.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()