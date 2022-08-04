<p align="center">
<img src="https://raw.githubusercontent.com/andriusluz/ameli-ai/main/ameliai_logo.png.png" width="100" height="100">

# Ameli-AI
</p>
*NOT READY FOR PRODUCTION/DAILY USE*

Welcome to Ameli-AI, a simple, beginner friendly but very ambitious voice assistant

Our goal is to run Ameli-AI in multiple devices such Linux, Windows, macOs, Android and iOs

Built with love and python3.10
Based on Knick-AI

## Features

- Cross platform (currently linux and partial windows support)
- Features Google for online speech recognition
- Vosk and pytssx3 for offline speech recognition
- Online text-to-speech with GoogleTTS
- Offline text-to-speech with RHVoice (Brazilian-Portuguese, Russian and Ukrainian voices)
- GUI available in KivyMD
- Cross platform
- Customizable Wake-word (like "OK Google" or "Hey Siri") support
- Integration with Google APIs like Google Calendar and Google Contacts
- WhatsApp Integration
- Multilingual (partially for now)
- StopDepression module (first voice assistant with this feature)
- Replaced keyboard module (used by Knick-AI) with pynput

## Installation

Install on linux with git:

```bash
sudo apt-get install python-dbus
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.10.0
asdf=/home/$USER/.asdf/bin/asdf
asdf update
asdf install python 3.10.5
asdf global python 3.10.5
asdf reshim python 3.10.5
pip install pipenv
asdf reshim python 3.10.5
asdf global python 3.10.5
git clone https://github.com/andriusluz/ameli-ai
cd ameli-ai
pipenv install
```
How to run:

```bash
pipenv shell
python main.py
```
    
## Roadmap

- Localization support (Weblate) - WIP
- TickTick and TodoIst integration - WIP
- A dockerized server appliance
- MusicBrainz support to get current playing music title
- Simple integration with IBM Watson and Amazon Polly for neural voices support - WIP
## Authors

- [@andriusluz](https://github.com/andriusluz)

