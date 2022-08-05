import os
import time
import playsound
import pyttsx3
import speech_recognition as sr
from gtts import gTTS

engine = 'gTTS'
lang_name = ''
lang_code = ''

def speak(text):
    if engine == 'gTTS':
        ttsvoice = gTTS(text=text, lang='en') # change lang here if you need
        filename = 'voice.mp3'
        ttsvoice.save(filename)
        playsound.playsound(filename)
    elif engine == 'pyttsx3':
        voice_pyttsx3 = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language='en-US') # you can change lang here
            #said = r.recognize_google(audio, language='pt-BR')
            print(said)
        except Exception as e:
            print(f"Exception: {str(e)}")
    return said

#speak('Olá Gab')

#text = get_audio()