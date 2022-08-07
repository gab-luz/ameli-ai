import time
import subprocess
import os
import playsound
import speech_recognition as sr
from sys import platform
from ext.console import intro_header
from googletts_voice import speak
import notify2
import constants

def assistant_introduction():
    print(intro_header)
    time.sleep(2)

def notify_ameli(message):
    notify2.init('Ameli-AI')
    n = notify2.Notification('Ameli-AI', message)
    n.show()
    
def take_command():     
		print("Listening.....")
		r = sr.Recognizer()
		r.dynamic_energy_threshold=False
		r.energy_threshold=4000
		r.pause_threshold = 1
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)
			audio = r.listen(source)
			said=""
		try:
			print("Recognizing.....")
			said = r.recognize_google(audio,language='en-us')
			print(f"You Said : {said}\n")
		except sr.UnknownValueError :
			print("could not understand audio \n ~Trying Again~")
			return take_command()
		except sr.RequestError as e:
			print("Could not request results, check your internet connection; {0}".format(e))
			return "None"

		return said.lower()

def wish_me():
    from datetoday import datetime
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        print("Hello, good morning")
        speak("Hello, good morning")
    elif hour >= 12 and hour < 18:
        print("Hello, good afternoon")
        speak("Hello, good afternoon")
    else:
        print("Hello, good evening")
        speak("Hello, good evening")

def note(text):
    from datetoday import datetime
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])

def any_random(var):
    import random
    return var[random.randint(0,len(var)-1)]
'''
USAGE for any_random(var) : 
hi=["Hello","Hi","Hey","Howdy","Hola","Bonjour"]
print(any_random(hi))
'''

def cleaner():
    if os.path.exists("pywhatkit_dbs.txt"):
        os.remove("pywhatkit_dbs.txt") #i don't know why this comes but yes, i'll remove it for sure xD
        #this function can be used to remove more unwanted folders too.