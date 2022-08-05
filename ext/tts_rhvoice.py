#!/usr/bin/env python3
import contextlib
from subprocess import call # to use on windows
from playsound import playsound
from rhvoice_wrapper import TTS
import os

with contextlib.suppress(Exception):
    os.remove('rhvoice_out.ogg')

def tts_rhvoice(text,voice):
    TTS().to_file('rhvoice_out.ogg', text = f'{text}', voice=f'{voice}', format_='opus', sets=None)
    playsound('rhvoice_out.ogg')

# !!!!!! probably if I want to use rhvoice, pyttsx3 and gtts, I must 
# create a single function mixing all of them

#TTS().to_file(filename='rhvoice_out.ogg', text='Isso é um teste', voice='Letícia-f123', format_='opus', sets=None)
#tts_rhvoice('teste', 'letícia-f123')
#playsound('rhvoice_out.ogg')
#print(TTS().voices)
#('alan', 'aleksandr', 'aleksandr-hq', 'anatol', 'anna', 'arina', 'artemiy', 'azamat', 'bdl', 'clb', 'elena', 'evgeniy-eng', 'evgeniy-rus', 'hana', 'irina', 'kiko', 'letícia-f123', 'lyubov', 'magda', 'marianna', 'mikhail', 'natalia', 'natan', 'nazgul', 'pavel', 'slt', 'spomenka', 'suze', 'talgat', 'tatiana', 'umka', 'victoria', 'vitaliy', 'vitaliy-ng', 'volodymyr', 'yuriy')