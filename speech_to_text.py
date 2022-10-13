import speech_recognition as sr
import pyttsx3
from naoqi import ALProxy
robot_IP = "192.168.0.101"
tts = ALProxy("ALTextToSpeech", robot_IP, 9559)

r = sr.Recognizer()

def speckText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def speech_to_text():
    while(1):
        try:
            # use microphone
            with sr.Microphone() as source2:
                print("Listening...")
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens to audio
                audio2 = r.listen(source2)

                # using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                print(MyText)
                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
            # tts.say("Oops! Didn't catch that")