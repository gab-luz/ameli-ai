# módulo para acomodar google tts, festival e rhvoice
import pyttsx3
from gtts import gTTS as tts
import pysound


#class voice(self,text,lang,country):

tts('Olá, tudo bem?',lang='pt')
tts.save('ola.mp3')
pysound('ola.mp3')

# https://scribe.nixnet.services/@ivaldobrandao/reconhecimento-de-fala-e-tts-offline-em-portugu%C3%AAs-8f2c67a71dfc