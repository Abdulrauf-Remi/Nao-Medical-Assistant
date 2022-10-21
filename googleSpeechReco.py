from google.cloud import speech
import io
# Instantiates a client
client = speech.SpeechClient()

 

def transcribe_speech():
    with io.open('output.wav', "rb") as audio_file:
        audio_file= audio_file.read()

    audio = speech.RecognitionAudio(content=audio_file)

    config = speech.RecognitionConfig(
      encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
      sample_rate_hertz=16000,
      language_code="en-US",)

  # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(result.alternatives[0].transcript)
    
transcribe_speech()