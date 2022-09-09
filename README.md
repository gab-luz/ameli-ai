<p align="center">
<img src="https://raw.githubusercontent.com/gab-luz/ameli-ai/main/ameliai_logo.png" width="100" height="100">

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
- Cross platform (Linux/Widows/macosx, support for android and ios also planned)
- Customizable Wake-word (like "OK Google" or "Hey Siri") support
- Integration with Google APIs like Google Calendar and Google Contacts
- Replaced keyboard module (used by Knick-AI) with pynput
- Replaced OpenWeatherMap (used by Knick-AI) with OpenMeteo, thus avoiding the use of an API key

## Commands implemented so far 
| Feature  | Description| Linux  | Windows  | macosx  |
|---|---|---|---|---|
| WakeWord  | Enables you to use your own customized hotword like "OK Google" or "Hey Siri" | X  | X  |X|
| AppFinder  | Lets you find your installed apps and perform actions with them.  | X  | Partial  |Partial|
| GoogleTTS (online text-to-speech) | Use Google's TTS Engine. Check supported languages. | X  | X  |X|
| RHVoice (offline text-to-speech)  |  Use RHVoice TTS Engine. Check supported languages. | In progress  |   ||
| Vosk (offline speech recognition)  | Use Vosk for speech recognitions. Check supported languages.  | In progress  |   ||
| (Partial) mpris support  | Currently, allows you to stop any compatible media player with mpris protocol. | X  |  ||
| Browser (like "open netflix")  | Enables you to open multiple websites. NavMode under progress (will take some time, might not even work :( ))  | X  | X  |X|
| Take screenshot  | Uses python to take screenshots of your screen.  | X  | X  |X|
| Humanized time/date questions (like <br />"what weekday is today", <br />"what year is this")  | Uses arrow to give you more humanized answers. Check available options.  | X  | X  |X|
| Computer actions | Supported actions: reboot, shutdown, logoff and open terminal / console /command prompt   | X  | X  |X|

## Available add-ons so far
| Feature  | Description| Linux  | Windows  | macosx  |
|---|---|---|---|---|
| LofiGirl*  | Allows you to focus better on your <br /> tasks when you're inside a noisy environment | X  | X  | X|

*I had to disable the original Lofi Girl extension I've done because it was getting video directly without ads, not allowing creators to monetize their content.

## Installation

Install on linux with git:

```bash
sudo apt-get install python-dbus libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 libplayerctl-dev libdbus-1-dev libdbus-glib-1-dev python3-pyaudio libcairo2-dev pkg-config python3-dev
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

Install on windows using scoop (check website https://scoop.sh):
```bash
(inside ameli-ai's folder)
Install on windows using scoop (check website https://scoop.sh):
(inside ameli-ai's folder)
scoop install git
scoop bucket add main
scoop install pyenv
pyenv install 3.10.5
pyenv global 3.10.5
python -m pip install pipenv
scoop reshim
pipenv install
```

Finally, to run:
```bash
pipenv shell
python main.py
```
**BEWARE WITH BUGS. YES, YOU'LL FIND A LOT OF THEM **
   
## Roadmap
- GUI available in KivyMD - WIP
- Localization support (Weblate) - WIP
- TickTick and TodoIst integration - WIP
- A dockerized server appliance
- MusicBrainz support to get current playing music title - WIP
- Simple integration with IBM Watson and Amazon Polly for neural voices support - WIP
- WhatsApp Integration - WIP
- Multilingual (partially for now) - WIP
- StopDepression module (first voice assistant with this feature) - WIP
## Authors

- [@gab-luz](https://github.com/gab-luz)

