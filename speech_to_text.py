import speech_recognition as sr
from naoqi import ALProxy
import wave
import pyaudio
robot_IP = "192.168.0.104"
tts = ALProxy("ALTextToSpeech", robot_IP, 9559)
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
    "type": "service_account",
    "project_id": "test-audio-362222",
    "private_key_id": "e0d51866069053b8cc63553541ca330fd10e3904",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCJvjGBP/VbhTx0\nQ5LMGmAjN/kwh3CUHIjlait4r5xbZCJQ+S28mFrbWnNo8MLpPyLpol7QJ8cpIBI6\nGSkt9EQeD59jqDxzJVVEqfiIJAhN2omvjmrUkRSP/aZSqSo5wLXA1LzoFrisXpxp\nFUghAlXgSiHC7U8MCGhSIUsUHAnB6YwnLWaF+Jj/Q2NO9FmmcFY2Rv9UDmx2xCjd\na2hXZj0/YWrsxG2l1+PvO4OsjQdRBs+09TuUA0gKaeB/dfSOaKDxEsEgjsmjdpg3\nPv8lyFzBUOwxlTCeXoxA6j/KKPPwFhTisEtdlhHsXwR9DkX1CPdUvERLX0fA6XGb\n5RSR5qlrAgMBAAECgf8uRbZbtSC3ngqxBAJMjo+9RRBxPQ6UswFKEGCKKnRcP0dH\n7G1w7b2X8srSdg8ETDFuSx2Oz84YAq4c1lb/GQ/JCXaCBAJKrD/40SCsm24uuTuH\nvlAlGJfPx2YYXrvQquxj2xOa5Acl4KKqqnuQmzg+IKk20oG7iReCf6y5FLIyccRr\n7U02FenaIOj8ogzAP9z35OlvqscKcZml9L8xmdaSlqskCz6xHUsxs5U2h3/XNHXj\nljOBzksGPS4PQCIg5tVKkIWHrY5AYO2GrWg5P9U+p3aUfTDr6IJNS99xUsFjzD9x\nbmC2UW7M2LgLYZ9Ur545mGNd/rXTbWX7T35jOwECgYEAwSra3fuz0pn3ZGt28E4u\nEN7UbLr2LD7GwA599qRuNlT0C/D2trdkR7dObFobpiYjaUQuHyBAHKCCHUzi7iA0\nC6QOICGnli9AApxOV/19fZLcYKchvH+29d7NUhBHeEyIG7lWXr7+U2M4ubh2i9Z5\n9RyfbLWiHVFHsn9fziZWe0ECgYEAtowdxqPoH+Ix6bU41ldeNc89WQ5w6sM8/V8h\n2XBx+n3+g4Kc8EavMCMaZ/Laa/kp8hFhoiBkgj6lqn6wN+gl0ELnayIHsK/xleOO\nnoWYGT7dmbo4mZhny1bJDz9AJirWfmXXexOXUAtLcco/apqp85m1zsQ59WNQtPaw\ngtqGFasCgYBNtCqE32qPzkW5TI10z04ylSCIeJDsbXhP68R6Ad0f1/6wCweDqrQZ\nMUDHz1uN84uNHdMbzEJeAac1mCc1ORkWkbDo9gDPJkSuiCfvt1XSvNAPxUuJ4yo7\nL5wSZeAKIWcjF+QJivUNoD1CYFS3ndhDZHcxKMOE3Zxkzl5AtCVXwQKBgQCo/w6R\n1ywOWFndAuibhkaxiipBSB1BOX49EtVDd9YNEJePKFwiFU4aQmUv1qRfUUyDzZOV\nhGeILHcyYBbDqydWppmXlOmJqVj+aqyeFQ+6T3jX2I6No4pztORuOSAqNX5dher3\nBiwO7mXp8lLDXmv4GVU3FnKRul/9KGRAwA1iAQKBgHSjwUoI8f5K9UNy/N2XRarV\nzvCZv6WZpJWMJ9+zvYJdW9Fg7nTXPnhdgzF/vrl7zCGVMF0BpwbHr3MwYCsgNHJ6\nVYynPJnI813Xvo1oOBNKWvwlFRxNzLhi+v1MkxN60QJqkFkbC/wpY34jZZd6YsBP\nnIPsxBC58AoFGYiFcYkK\n-----END PRIVATE KEY-----\n",
    "client_email": "myservice@test-audio-362222.iam.gserviceaccount.com",
    "client_id": "114327203511964146760",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/myservice%40test-audio-362222.iam.gserviceaccount.com"
  }
"""

r = sr.Recognizer()



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
            # with sr.Microphone() as source:
            with sr.AudioFile('output.wav') as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.2)

                # listens to audio
                audio = r.listen(source)

                # using google to recognize audio
                MyText = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
                MyText = MyText.lower()
                print(MyText)
                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
            # tts.say("Oops! Didn't catch that")



