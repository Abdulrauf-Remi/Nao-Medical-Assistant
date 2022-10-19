import speech_recognition as sr
from naoqi import ALProxy
from os import path
from audio_speechrecognition import record_NAO
import wave
#WAV_FILE = path.join(path.dirname(path.realpath(__file__)), "comeOn.wav")
robot_IP = "192.168.0.108"
tts = audio = record = aup = None
tts = ALProxy("ALTextToSpeech", robot_IP, 9559)
def speech_recognition():
    try:
        global speechRecWord_rec
        print("you can say now...")
        tts.say("you can say now...")
        record_NAO(robot_IP, robot_PORT=9559)
        # audio = ALProxy("ALAudioDevice", robot_IP, 9559)
        WAV_FILE = "record.wav"
        r = sr.Recognizer()
        #m = sr.Microphone()
        # nao_mic = audio.openAudioInputs()
        m = sr.AudioFile(WAV_FILE)
        #print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold
            #print("Set minimum energy threshold to {}".format(r.energy_threshold))
            audio_to = r.listen(source)
            #print("Got it!")
            try:
                # recognize speech using Google Speech Recognition
                global speechRecWord_rec
                speechRecWord_rec = r.recognize_google(audio_to)
                print(speechRecWord_rec)

            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
                tts.say("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        pass
    return speechRecWord_rec

speech_recognition()