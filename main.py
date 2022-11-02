# Libraries
from naoqi import ALBroker, ALProxy
import time
import sys


# external Python files
import speak
import move
import faceDetect
from speech_to_text import speech_to_text
# import googleSpeechReco
import movement
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


def main():

    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       NAO_IP,          # parent broker IP
       NAO_port)        # parent broker port
       
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
    global movement
    movement = movement.Dialog(moveModule)
    
    
    # set face tracking (only work when NAO Auto-life enabled)
    faceProxy = ALProxy("ALFaceDetection")
    faceProxy.enableTracking(True)

    #  animatedSpeechProxy = ALProxy("ALAnimatedSpeech", NAO_IP, NAO_port)
    #  configuration = {"bodyLanguageMode":"contextual"}




    fever_follow = "Do you have any other symptoms such as abdominal pain, rashes or faint pink spots, usually on your chest or stomach, cough, diarrhea or constipation"
    typhoid_true = "Then you have typhoid fever"
    
    # LOOP
    try:

        while True:
            human_input = speech_to_text()     # reveive transcript that contains keyword
            if "dance" in human_input:
                speakModule.say(movement.answer(human_input))
            elif "sit down" in human_input:
                speakModule.say(movement.answer(human_input))
            elif "stand up" in human_input:
                speakModule.say(movement.answer(human_input))

            resp = requests.post("http://localhost:5000/predict", data=human_input)
            
            print(resp.text)
            speakModule.say(str(resp.text))
            # speakModule.say(str(resp.text)) # react to the transcript 
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

            if "depression" in str(resp.text):
                print("Depression is a mood disorder that causes a persistent feeling of sadness and loss of interest. Also called major depressive disorder or clinical depression, it affects how you feel, think and behave and can lead to a variety of emotional and physical problems.")
                speakModule.say("Depression is a mood disorder that causes a persistent feeling of sadness and loss of interest. Also called major depressive disorder or clinical depression, it affects how you feel, think and behave and can lead to a variety of emotional and physical problems.")
                time.sleep(1)
                print("Do you have trouble doing normal day-to-day activities, and sometimes you feel as if life isn't worth living.")
                speakModule.say("Do you have trouble doing normal day-to-day activities, and sometimes you feel as if life isn't worth living.")
                depressfans = speech_to_text()
                if "yes" in depressfans:
                    print("Okay, I make an appointment to see a mental health professional as soon as possible.")
                    speakModule.say("Okay, I make an appointment to see a mental health professional as soon as possible.")
                    time.sleep(1)
                    print("If you think you may hurt yourself or attempt suicide. Please, consider these options")
                    speakModule.say("If you think you may hurt yourself or attempt suicide. Please, consider these options")
                    time.sleep(1)
                    print("Call your doctor immediately, Reach out to a close friend or loved one, or contact a spiritual leader or someone else in your faith community.")
                    speakModule.say("Call your doctor immediately, Reach out to a close friend or loved one, or contact a spiritual leader or someone else in your faith community.")

                else:
                    depress_ques = "medicine for depression"
                    resp = requests.post("http://localhost:5000/predict", data=depress_ques)
                    print(resp.text)
                    speakModule.say(str(resp.text))

                    depress_ques = "What to eat to avoid getting depression"
                    resp = requests.post("http://localhost:5000/predict", data=depress_ques)
                    print(resp.text)
                    speakModule.say(str(resp.text))

                    depress_ques = "any preventions for depression"
                    resp = requests.post("http://localhost:5000/predict", data=depress_ques)
                    print(resp.text)
                    speakModule.say(str(resp.text))
                    time.sleep(2)
                    speakModule.say("Please, you may go to the pharmacy for your medication")


            if "diabetes" in str(resp.text):
                print("Diabetes is a chronic disease that occurs either when the pancreas does not produce enough insulin or when the body cannot effectively use the insulin it produces.")
                speakModule.say("Diabetes is a chronic disease that occurs either when the pancreas does not produce enough insulin or when the body cannot effectively use the insulin it produces.")
                time.sleep(1)
                print("I will suggest you go to the laboratory for a blood test to check your your glucose level")
                speakModule.say("I will suggest you go to the laboratory for a blood test to check your your glucose level")
                time.sleep(2)
                speakModule.say("Do you have other symptoms you've not mention")
                depressfans = speech_to_text()

                print("Okay, your blood test will determines if you have prediabetes")
                speakModule.say("Okay, your blood test will determines if you have prediabetes")
                time.sleep(1)
                print("If the laboratory test determines you have prediabetes, you and your doctor will work together to make lifestyle changes such as weight loss, exercise, healthy diet to prevent or delay developing Type 2 diabetes.")
                speakModule.say("If the laboratory test determines you have prediabetes, you and your doctor will work together to make lifestyle changes such as weight loss, exercise, healthy diet to prevent or delay developing Type 2 diabetes.")
                
                time.sleep(2)
                print("Regardless of the result of your blood test, please take note of the follwing information to maintain a normal glucose level")
                speakModule.say("Regardless of the result of your blood test, please take note of the follwing information to maintain a normal glucose level")
                
                depress_ques = "What to eat to avoid getting diabetes"
                resp = requests.post("http://localhost:5000/predict", data=depress_ques)
                print(resp.text)
                speakModule.say(str(resp.text))

                depress_ques = "any preventions for diabetes"
                resp = requests.post("http://localhost:5000/predict", data=depress_ques)
                print(resp.text)
                speakModule.say(str(resp.text))
            


 	    
    except KeyboardInterrupt:
    	
        print ("Interrupted by user, shutting down")
        myBroker.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()