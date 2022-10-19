import speech_recognition as sr
import pyttsx3
from naoqi import ALProxy
import wave
import pyaudio
robot_IP = "192.168.0.108"
tts = ALProxy("ALTextToSpeech", robot_IP, 9559)

r = sr.Recognizer()

def speckText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def mic_stream():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1

    fs = 16000 # Record at 16000 samples per second
    seconds = 6
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()



def speech_to_text():
    while(1):
        try:
            # use microphone
            mic_stream()
            with sr.AudioFile('output.wav') as source2:
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