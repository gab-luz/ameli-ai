import time
import subprocess
import os
import playsound
import speech_recognition as sr
from sys import platform
from ext.console import intro_header
from googletts_voice import speak
import notify2

def assistant_introduction():
    print(intro_header)
    time.sleep(2)
# def notify(message):
#     if platform in ['linux','linux2']:
#         subprocess.Popen([f"notify-send 'Ameli-AI' {message}", shell := True])
#     if platform == 'win32':
#         from win10toast import ToastNotifier
#         # create an object to ToastNotifier class
#         n = ToastNotifier()
#         n.show_toast("Ameli-AI", {message}, duration = 10)
#     if platform == 'darwin':
#         host_va = 'Ameli-AI'
#         subprocess.Popen([f"osascript -e \'display notification {message} with title \"{host_va}\"'", shell := True])

# notify2.init('app name')
# n = notify2.Notification('title', 'message')
# n.show()

def notifyAmeli(message):
    notify2.init('Ameli-AI')
    n = notify2.Notification('Ameli-AI', message)
    n.show()
    
def takeCommand():     
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
			return takeCommand()
		except sr.RequestError as e:
			print("Could not request results, check your internet connection; {0}".format(e))
			return "None"

		return said.lower()

def wishMe():
    from datetoday import datetime
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        print("\n")
        print("Hello,Good Morning")
        speak('Hello. Good morning')
    elif hour>=12 and hour<18:
        print("\n")
        print("Hello,Good Afternoon")
        speak("Hello,Good Afternoon")
    else:
        print("\n")
        print("Hello,Good Evening")
        speak("Hello,Good Evening")

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
def desktop_notification(text_for_notification,duration_of_notification):
    # import win10toast
    if platform == 'win32':
        from win10toast import ToastNotifier
        # create an object to ToastNotifier class
        n = ToastNotifier()
        n.show_toast("Ameli-AI",text_for_notification, duration = duration_of_notification)
    else:
        print('Not implemented yet.')

def cleaner():
    if os.path.exists("pywhatkit_dbs.txt"):
        os.remove("pywhatkit_dbs.txt") #i don't know why this comes but yes, i'll remove it for sure xD
        #this function can be used to remove more unwanted folders too.