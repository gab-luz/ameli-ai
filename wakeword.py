import os
import speech_recognition as sr
from sys import platform
import notify2
import rich
from main import start_from_hibernation
from common import notify_ameli

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
			print("\n~Trying again~")
			return background_listening()
		except sr.RequestError as e:
			print("Could not request results, check your internet connection; {0}".format(e))
			return "None"    
		return said.lower()



def work_in_background():
		notify_ameli('Assistant is not working in background')
		while True:
				Listening=background_listening()
				if Listening not in hotwords:
						continue
				notify_ameli("Assistant is now running in foreground")
				start_from_hibernation()
				break  


if __name__ == '__main__':
	work_in_background()

