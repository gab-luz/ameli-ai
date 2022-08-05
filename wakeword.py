
#this file uses a .pyw extension to run in the background

import os
import speech_recognition as sr
from sys import platform
import notify2
import rich
from main import start_from_hibernation


notify2.init('app name')
n = notify2.Notification('title', 'message')
n.show()

def background_listening():
		print("Listening in background....")
		r = sr.Recognizer()
		r.dynamic_energy_threshold=False
		r.energy_threshold=4000
		r.pause_threshold = 0.5
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)
			audio = r.listen(source)
			said=""
		try:
			print("Recognizing in background....")
			said = r.recognize_google(audio,language='en')
			print(f"You Said : {said}\n")
			if said in hotwords:
				start_from_hibernation()
		except sr.UnknownValueError :
			print("\n~Trying Again~")
			return background_listening()
		except sr.RequestError as e:
			print("Could not request results, check your internet connection; {0}".format(e))
			return "None"    
		return said.lower()

def desktop_notification(text_for_notification,duration_of_notification):
    if platform == 'win32':
        # import win10toast
        from win10toast import ToastNotifier
        # create an object to ToastNotifier class
        n = ToastNotifier()
        n.show_toast("AmeliAI",text_for_notification, duration = duration_of_notification)
    else:
        print(text_for_notification)

hotwords=[
    'assistant activate',
    'wake up assistant',
    'hey Ameli',
    'OK Ameli',
    'wake up Ameli'
]

def work_in_background():
		desktop_notification("Assistant running in background",5)
		while True:
				Listening=background_listening()
				if Listening not in hotwords:
						continue
				desktop_notification("Assistant is now running in foreground",4)
				start_from_hibernation()
				break  


if __name__ == '__main__':
	work_in_background()

