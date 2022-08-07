import requests
from sys import platform
from googletts_voice import speak, get_audio
from datetime import datetime
import webbrowser
from dialogue import *
import os
from playsound import playsound
import pywhatkit
from ext.tts_rhvoice import tts_rhvoice
from pynput.keyboard import Key, Controller
from pynput import keyboard
import re
import wikipedia
import urllib
import urllib3
import json
import subprocess
from main import start_from_hibernation
from rich import print as rprint
from wakeword import background_listening, work_in_background
from constants import *
import git
import time
import arrow #https://arrow.readthedocs.io/en/latest/

#preferences [will be stored in userdata.db]
you = 'Sir'
maps_provider = 'googlemaps'
news_url="https://news.google.com/news/rss"
your_lang = 'en-US'
api_key_unsplash = ''
api_key_spotify = ''


g = git.cmd.Git(os.getcwd())

#tts_rhvoice('Tudo bem? O que você precisa?','letícia-f123')
# text = get_audio().lower()

# def note(text):
#     date = datetime.datetime.now()
#     file_name = str(date).replace(":","-") + "-note.txt"
#     with open(file_name,"w") as f:
#         f.write(text)
#         if platform in ["linux", "linux2"]:
#             subprocess.Popen(["gedit",file_name])
#         elif platform == "darwin":
#             print('Ameli is not available to macOs users yet. Sorry.')
#         elif platform == "win32":
#             subprocess.Popen(["notepad.exe",file_name])
            
# NOTE_STRS = ['make a note','write this down','remember this']
# for phrase in NOTE_STRS:
#     if phrase in NOTE_STRS:
#         if phrase in text:
#             speak('What would you like me to write down?')
#             note_text = get_audio().lower()
#             note(note_text)

def ameli_response(audio):
    print(audio)
    for line in audio.splitlines():
        os.system(f"say {audio}")
            
def any_random(var): # it will randomize stuff you want as var
    import random
    return var[random.randint(0,len(var)-1)]
'''
USAGE for any_random(var) : 
hi=["Hello","Hi","Hey","Howdy","Hola","Bonjour"]
print(any_random(hi))
'''
            
def showmagic():
    #didn't remove it, just in case
    while True:
        ask=any_random(asking)
        print("\n",ask)
        speak(ask+".")
        statement=get_audio().lower()

        if statement==None:
            print("No Input Detected!\n")
            continue
 
        elif "good bye" in statement or "ok bye" in statement or "bye" in statement or "quit" in statement:
            print("\n")
            print('    Your Personal Assistant Ameli is shutting down, goodbye.     ')
            speak('Your Personal Assistant Ameli is shutting down, goodbye.')
            time.sleep(4)
            quit()
        
        elif "pause" in statement or "please pause" in statement:
            speak("Assistant paused.")
            print("OK. I am paused.\nPress 'W' whenever You Want Me to Resume")
            print("  ")
            from console import assistant_pause,assistant_resumed
            print(assistant_pause)
            print("  ")
            while True:
                background_listening()
                def on_activate_w():
                    speak("Assistant resumed.")
                    speak(assistant_resumed)
                    start_from_hibernation()
                with keyboard.GlobalHotKeys({
                    'w': on_activate_w}) as h:
                    h.join()
                    
                    showmagic()
                
        elif statement in ["no thanks","no","not now","leave me alone","shut up","stay quiet","sleep","hibernate"]:
            speak("OK, I will sleep for some time then.")
            print("OK, I will sleep for some time then.")
            speak("Use the wakeword to awake me, till then I'll be silent.")
            print("Use the wakeword to awake me, till then I'll be silent.")
            print("If you want to know the wake words available, say Yes.")
            speak("If you want to know the wake words available, say Yes.")
            wakeword_confirmation = get_audio()
            if wakeword_confirmation == 'yes':
                print("OK. I'll tell you the available wake words, honey.")
                speak("OK. I'll tell you the available wake words, honey.")
                for custom_wakeword in hotwords:
                    speak(custom_wakeword)
                    print(custom_wakeword)
            else:
                time.sleep(2)
                work_in_background()
                quit()

        elif "hi"==statement or "hello" in statement :
            hello_greeting=any_random(hello)
            print(hello_greeting,"\n(NOTE:if you wanna have chat with me. just use the 'Lets Chat' command)")
            speak(hello_greeting)
            time.sleep(1)
            
        elif statement in ['stop music', 'stop media','stop podcast']:
            if platform == 'win32':
                import win32api
                VK_MEDIA_PLAY_PAUSE = 0xB3
                stop_media_win = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
                win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, stop_media_win)
                print('OK. Media has been stopped.')
                speak('OK. Media has been stopped.')
            elif platform in ['linux','linux2']:
                subprocess.call('playerctl --all-players stop',shell=True)
                print('OK. Media has been stopped.')
                speak('OK. Media has been stopped.')
                time.sleep(2)
            else:
                print('Not implemented yet.')
                speak('Not implemented yet.')
                
                            
        elif "open netflix" in statement:
                print('OK. Opening Netflix...')
                speak('Ok. Opening Netflix...')
                webbrowser.open_new_tab("https://www.netflix.com")
                time.sleep(3)
                print("OK. Netflix is open now.")
                speak('OK. Netflix is open now.')
                    

        elif "open youtube and search for" in statement or "open youtube and search" in statement:
                query=statement.split('open youtube and search for')
                srch=query
                print("Searching for : ",srch," on youtube")
                print("opening youtube...")
                sss=(f"https://www.youtube.com/results?search_query="+
                        "+".join(srch))
                pywhatkit.playonyt(sss)
                time.sleep(1)

        elif 'open youtube' in statement:
                print('Opening Youtube...')
                speak('Ok. I\'ll open it.')
                webbrowser.open_new_tab("https://www.youtube.com")
                time.sleep(3)
                print("youtube is open now.")
                time.sleep(5)
       
        elif 'open github' in statement:
            print('Opening GitHub...')
            webbrowser.open_new_tab("https://github.com/")
            print('GitHub is now Open.')
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            print("Google chrome is open now.")
            time.sleep(5)

        elif "snipping tool" in statement:
            if platform == 'win32':
                speak("Opening Snipping Tool")
                print("Opening Snipping Tool")
                os.system("start snippingtool")
                time.sleep(5)
            else:
                speak("The snipping tool is available only for Windows Users. \
                      I'm sorry, but I can't open it.")

        elif "screenshot" in statement:
            import random
            time.sleep(1.5)
            import pyscreenshot
            image = pyscreenshot.grab()
            r = random.randint(1,20000000)
            file_name=("ameliscreenshot"+ str(r) +".png")
            image.save(file_name)
            print("Screenshot saved as : ",file_name)
            speak(f'OK. The screenshot was saved as: {file_name}')
            speak('Task completed. Want to open the screenshot file? Say Yes or No, please.')
            print('Task completed. Want to open the screenshot file? Say Yes or No, please.')
            scrnshot_image=get_audio().lower()
            time.sleep(2)
            if "yes" in scrnshot_image:
                speak('OK. Your wish is my command.')
                if platform in ['linux','linux2']:
                    call(['xdg-open',file_name])
                if platform == 'darwin':
                    print('Ameli is not fully supported in macOs yet. Sorry.')
                    speak('Ameli is not fully supported in macOs yet. Sorry.')
                if platform == 'win32':
                    subp.call(file_name, shell=True)
            elif "no" in scrnshot_image:
                speak('OK. Maybe later.')
            time.sleep(2)

        elif "handwriting" in statement:
            speak("Enter the text you want to Convert ?")
            vars=input("Enter the Text which you want to convert into Your Handwriting. \n>>")
            pywhatkit.text_to_handwriting(string=vars,save_to="handwriting.png")
            print("Your Text to HandWriting Conversion is Done!\nTIP: To check your Result, Check for handwriting.png File")
            time.sleep(3)

        elif "image conversion" in statement :
            ima=input("Enter the Path of Image :")
            pywhatkit.image_to_ascii_art(imgpath=ima,output_file="ameli_asciiart.txt")
            print("i have Made Your ASCII art and also saved it.")
            time.sleep(3)

        elif "edge" in statement:
            if platform == 'win32':
                print("Opening Microsoft Edge")
                os.system("start msedge")
                time.sleep(5)
            else:
                speak("If you're asking to open Microsoft Edge, know that this is not available \
                      for your operating system.")

        elif 'open whatsapp' in statement or 'whatsapp' in statement:
            webbrowser.open_new_tab('https://web.whatsapp.com/')
            print('opening WhatsApp Web')
            time.sleep(6)

        elif 'open instagram' in statement or 'instagram' in statement:
            webbrowser.open_new_tab('https://www.instagram.com/')
            print('opening Instagram')
            time.sleep(6)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            print("Google Mail is open now.")
            time.sleep(5)

        elif 'open discord' in statement or 'discord' in statement:
            webbrowser.open_new_tab("https://discord.com/channels/@me")
            print("discord is open now.")
            time.sleep(5)

        elif 'open facebook' in statement:
            print('opening facebook...')
            webbrowser.open_new_tab("https://www.facebook.com/")
            print('facebook is open now.')
            time.sleep(5)

        elif "open stackoverflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            print("Here is stackoverflow")
            time.sleep(3)

        elif 'clear cache' in statement or 'clear system cache' in statement or 'boost system' in statement:
            speak("Clearing system Cache....")
            speak("please do not touch anything for a while, the automated process is starting.")
            keyboard.press_and_release('win+R')
            time.sleep(1)
            keyboard.write("%temp%",delay=0.1)
            time.sleep(0.7)
            keyboard.press_and_release("enter")
            print("clearing cache in process....")
            time.sleep(2.6)
            keyboard.press_and_release("ctrl+a")
            time.sleep(0.5)
            keyboard.press_and_release("del+shift")
            time.sleep(0.7)
            keyboard.press_and_release("enter")
            print ('Starting the removal of the file !\n')
            print("If you see any Error, just Delete the Temp Folder manually.")
            time.sleep(3)

        elif "open my inbox" in statement:
            webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#inbox")
            time.sleep(3)

        elif "open my sent mails" in statement or "open my sent mail" in statement:
            webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#sent")
            time.sleep(3)

        elif 'open terminal' in statement or 'cmd' in statement or 'open console' in statement:
            if platform in ['linux','linux2']:
                try:
                    subprocess.call('xfce4-terminal', shell=True)
                    speak("Terminal is open")
                except Exception:
                    subprocess.call('gnome-terminal', shell=True)
                    speak("Terminal is open")
            if platform == 'darwin':
                print('Not implemented yet. Please open an issue about it.')
                speak("Not implemented yet. Please open an issue about it.")
            else:
                os.system('cmd')
                print("Command prompt is open Now")
                speak("Terminal is open")
                time.sleep(3)
                
        elif statement in ("the weekday","the day of the week"):
            today_date = arrow.utcnow()
            day_week = str(today_date.format('dddd'))
            print(f"Today is {day_week}")
            speak(f"Today is {day_week}")

        elif statement in ("tell me day","what day is today","tell me the date"):
            today_date = arrow.utcnow()
            day_day = str(today_date.format('MMMM DD, YYYY'))
            print(f"Today is {day_day}")
            speak(f"Today is {day_day}")
            
        elif statement in ('tell me the year'):
            a = arrow.utcnow()
            year_time = str(a.year)
            speak(f"We\'re in {year_time}.")
            print(f"We\'re in {year_time}.")

        elif 'log off' in statement or 'sign out' in statement:
            subprocess.call(["shutdown", "/l"])
        
        elif "shutdown" in statement or "shut down" in statement:
            speak('OK. Shutting down.')
            if platform in ['linux','linux2']:
                time.sleep(3)
                os.system('poweroff')
            if platform == 'win32':
                time.sleep(3)
                os.system('shutdown/s')
            if platform == 'darwin':
                time.sleep(3)
                os.system('shutdown -r')

        elif "restart my pc" in statement:
            speak("okay, restarting your pc")
            if platform in ['linux','linux2']:
                os.system('reboot')
            if platform == 'win32':
                os.system('shutdown/r')
        
        elif 'date today' in statement or 'today date' in statement:
            from datetoday import today_date
            print(today_date())
            speak(today_date())
            time.sleep(3)
        
        elif "empty recycle bin" in statement:
            if platform in ['linux','linux2']:
                os.system("rm -rf ~/.local/share/Trash/*")
                subprocess.call('start scripts/Hotword/hotword_detection.pyw', shell=True)
            elif platform in ['darwin']:
                os.system("sudo rm -rf ~/.Trash/*")
            elif _platform == "win32":
                print('Windows:')
                try:
                    os.system("rd /s c:\$Recycle.Bin")  # Windows 7 or Server 2008
                except:
                    pass
                try:
                    os.system("rd /s c:\recycler")  #  Windows XP, Vista, or Server 2003
                except:
                    pass
            else:
                print(_platform)
                speak("I'm trying to empty your recycle in. Press enter if any dialog box appears.")
                time.sleep(1.3)
                speak("Recycle bin now empty.")
                
        elif "note" in statement or "remember this" in  statement:
                print("What would you like me to write down?")
                speak("What would you like me to write down?")
                note(note_text)
                print("I have made a note of that.\n")

        elif "weather" in statement:
            #API KEY REQUIRED HERE
            if weather_api_key=="YOUR API KEY HERE":   #{this part can be comment out later,and indexing below shall be fixed
                print("You need to get an API key first!\n")
                break
            else:                                      #}
                base_url="https://api.openweathermap.org/data/2.5/weather?"
                print("\nwhats the city?")
                complete_url=base_url+"appid="+weather_api_key+"&q="+city_name     #weather_api_key is the api key here
                response = requests.get(complete_url)
                x=response.json()
                if x["cod"]!="404":
                    y=x["main"]
                    current_temperature = y["temp"]
                    current_humidiy = y["humidity"]
                    weather_description = (x["weather"])[0]["description"]
                    print(" Temperature in kelvin unit = " +
                        str(current_temperature) +
                        "\nhumidity (in percentage) = " +
                        str(current_humidiy) +
                        "\ndescription = " +
                        str(weather_description))
                    speak("Temperature in kelvin unit is " +
                        str(current_temperature) +
                        "\nhumidity in percentage is " +
                        str(current_humidiy) +
                        "\ndescription  " +
                        str(weather_description))

                else:
                    speak(" Location not found. ")
                    print(" Location not found ")

        elif "search on google" in statement:
                statement = statement.split("search on google")
                search = statement
                webbrowser.open("https://www.google.com/search?q=" + "+".join(search))
                speak("Searching " + str(search) + " on google")
                time.sleep(3)
                               
        elif 'open Reddit' in statement:
                reg_ex = re.search('open reddit (.*)', statement)
                url = 'https://www.reddit.com/'
                if reg_ex:
                    subreddit = reg_ex.group(1)
                    url = url + 'r/' + subreddit
                    webbrowser.open(url)
                    speak(f'The Reddit content has been opened for you, {you}.')

        elif 'ask' in statement:
            if wolfram_api_key=="YOUR API KEY HERE":
                print("You need to get an API key first!")
                break
            else:
                speak("I can answer to computational and geographical questions and what question do you want to ask now")
                client = wolframalpha.Client(wolfram_api_key) #API KEY REQUIRED HERE
                res = client.query(query)
                answer = next(res.results).text
                print(answer)
                
        elif 'change wallpaper' in statement:
            #folder = '/Users/nageshsinghchauhan/Documents/wallpaper/'
            folder_wallpapers = '~/wallpapers'
            for the_file in os.listdir(folder_wallpapers):
                file_path = os.path.join(folder_wallpapers, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
            api_key = 'fd66364c0ad9e0f8aabe54ec3cfbed0a947f3f4014ce3b841bf2ff6e20948795'
            url = 'https://api.unsplash.com/photos/random?client_id=' + api_key #pic from unspalsh.com
            f = urllib3.urlopen(url)
            json_string = f.read()
            f.close()
            parsed_json = json.loads(json_string)
            photo = parsed_json['urls']['full']
            urllib.urlretrieve(photo, folder_wallpapers) # Location where we download the image to.
            subprocess.call(["killall Dock"], shell=True)
            ameli_response('wallpaper changed successfully')
            
        # elif 'tell me a joke' in statement:

        #elif 'suggest me a movie' in statement:
            
        elif "I'm bored" in statement:
            bored_api = requests.get('https://www.boredapi.com/api/activity', verify=False)
            bored_api_activity = bored_api.json()
            print(bored_api_activity['activity'])
            speak(bored_api_activity['activity'])
        
        elif statement in ['wikipedia','who is ','what is ','who was ']:
            speak("Searching Wikipedia about it...")
            statement =statement.replace("search on wikipedia about", "")
            try:
                results = wikipedia.summary(statement, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except:
                speak("Unable to fetch date. Ask me maybe another time. I'm really sorry.")
                continue
            
        # build a screen recorder here
        
        elif statement in ["what time is it"]:
            time_now = datetime.today().strftime("%H:%M %p")
            speak(f"Well, it's {time_now}")
            print("Current Time =", time_now)

        elif 'news for today' in statement or 'tell me the news' in statement or 'read the news please' in statement:
            try:
                Client=urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"xml")
                news_list=soup_page.findAll("item")
                for news in news_list[:15]:
                    ameli_response(news.title.text.encode('utf-8'))
            except Exception as e:
                print(e)

        elif 'where is' in  statement:
            ind = statement.split().index("is")
            location = statement[ind + 8:]
            if maps_provider == 'googlemaps':
                url = "https://www.google.com/maps/place/" + "".join(location)
            else:
                url = "https://www.openstreetmap.org/search?query=" + "".join(location)
            speak("This is where I found, " + str(location))
            webbrowser.open(url)    
            time.sleep(3)

        elif 'yt studio' in statement or 'open yt studio' in statement or 'open youtube studio' in statement:
            webbrowser.open_new_tab("https://studio.youtube.com/")
            speak("opening youtube creator studio")
            
            time.sleep(5)

        elif 'keyword' in statement or 'google trends' in statement or 'keyword research' in statement:
            speak("do you want me to open google trends for keyword research.")
            print('type yes or no for Opening Google Trends')
            gtask=input('>> ')
            if (gtask=='yes'):
                webbrowser.open_new_tab('https://trends.google.com/')
            elif(gtask=='no'):
                speak("ok, i will not open Google Trends.")
                print("OPENING GOOGLE TRENDS : Cancelled By User")
            
            time.sleep(5)
              
        elif 'how were you born' in statement  or 'why were you born' in statement:
            print('''
            I was born on june 2021 by A Boy Who Had an Ambition To Change This World with the
            Help Of Artificial Intelligence, Although i am still just a small step towards this
            new ERA of A.I . But I am still Happy to be Born and serve you right now''')
            time.sleep(3)
        
        elif 'who are you' in statement or 'what can you do' in statement:
            print('I am Ameli, your Personal AI assistant. I am programmed for managing normal tasks in your life')
            speak("I am Ameli, your Personal AI assistant. I am programmed for managing normal tasks in your life")
            time.sleep(3)

        elif 'your name' in statement or 'what is your name' in statement :
            speak("my name is Ameli, how could you forget me :-(")
            print('my name is Ameli your A.I assistant')
            print(" (ㆆ_ㆆ) "*3)
            time.sleep(3)

        elif 'what is your slogan' in statement or 'what is your motive' in statement:
            print('Leading towards a efficient life.')
            time.sleep(3)
        
        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            print("I was built by Mr. Gab, based on Knick-AI, made originally by Arsh.")
            speak("I was built by Mr. Gab, based on Knick-AI, made originally by Arsh.")
            time.sleep(2)

        elif 'update ameli' in statement or 'update yourself' in statement:
            speak("Are you sure about it? \
                  Updating myself can be very dangerous. \
                  I suggest you check my webpage first. \
                  Say Yes for updating or No to stop.")
            update_yes_no=get_audio().lower()
            time.sleep(2)
            if "yes" in update_yes_no:
                print("OK. I'm updating myself.")
                speak("OK. I'm updating myself.")
                g.pull()
                if "up-to-date" in g.pull():
                    print("Ameli-AI already updated.")
                    speak("Ameli-AI already updated.")
                time.sleep(4)
            else:
                print("OK. Maybe another time.")
                speak("OK. Maybe another time.")

        elif 'tell commands' in statement or 'your commands' in statement  or 'command' in statement:
            speak("Telling you the list of my commands :")
            speak("below is the list of all commands respectively.")
            print('\n\nbelow is the list of all commands respectively')
            from console import command_list
            print(command_list)
            time.sleep(3)
        
        elif 'chat' in statement: 
            #print('\nChat Feature is Still in ALPHA vesion,\nso please have patience while using it.')
            from console import bug
            print(bug)
            time.sleep(3)
   
        elif 'play game' in statement:
            speak('opening mini games manager') 
            from minigames import minigamesmanager
            minigamesmanager.playgame()
            time.sleep(3)

        elif 'insult me' in statement:
            try:
                evil=''
                evil=requests.get(url='https://evilinsult.com/generate_insult.php?lang=en&type=json')
                data=evil.json()
                insult=data['insult']
                print(insult)
                speak(insult)
                print('This insult was done by evilinsult.com, not by us.')
                speak('This insult was done by evilinsult.com, not by us.')
                time.sleep(2)
            except:
                print("the insult generation server is down,you may try again later.")
                speak("I'm afraid I can't do it right now. Maybe... another time?")

        elif 'i want to dictate' in statement:
            speak("okay opening dictation option.")
            time.sleep(0.5)
            keyboard.press_and_release('win+H')
            time.sleep(0.5)
            continue

        elif 'say' in statement or 'pronounce' in statement:
            speak("okay, type the text.")
            what_to_say=input('What you Want Me To Say : ')
            print('user entered :',what_to_say)
            speak(what_to_say)
            time.sleep(2)

        elif "change input mode" in statement:
            speak("ok, select the input mode again.")
            showmagic()

        elif "thanks" in statement:
            reply_to_thanks=any_random(np)
            print(reply_to_thanks)
            speak(reply_to_thanks)
            
        elif statement in {"depressed","I'm depressed","I'm very depressed"}:
            speak("Oh. Do you want to talk about it? I’m here when you’re ready.")
            depressed_audio=get_audio().lower()
            time.sleep(2)
            if "yes" in depressed_audio:
                speak('You’re not alone — I may not understand exactly how you feel, but you’re not alone')
                speak("There's not much I can do for now. Maybe I can play a music playlist, ok?")
                depressed_audio2=get_audio().lower()
                if "yes" or "ok" or "sure" or "do it" or "please" in depressed_audio2:
                    speak("OK. I'll open a YouTube playlist. I want to make you feel better.")
                    print('OK. I\'ll open a YouTube playlist. I want to make you feel better.')
                    #webbrowser.open_new_tab("https://www.youtube.com/embed/9qDfg041D20?autoplay=1")
                    pywhatkit.playonyt('9qDfg041D20')
                    time.sleep(3)
                    print("youtube is open now.")
                    time.sleep(5)
                else:
                    speak("Oh, I see. Please get some help. Okay?")
            elif "no" in depressed_audio:
                speak('Oh, I see. Please get some help. Okay?')
            time.sleep(2)
                 
        elif statement in ("focus","help me focus please","I can't focus"):
            speak("Oh, I see. There's a lot of ways I can help you focusing \
                on your tasks. For instance, if you want to minimize all your \
                windows and get absolute focus on your tasks, you can say \
                distraction-free mode, please. \
                Or maybe you want to start a pomodoro timer, right? \
                In that case, say start pomodoro timer please. \
                Additionally, I can also play a lofi song \
                by opening a Lofi Girl's livestream on YouTube, \
                you just have to say Lofi Girl. \
                So tell me what will be your choice for now {you}. \
                ")
        elif statement in ("lofi girl", "lo-fi girl","low-fi girl"):
            speak("OK. Opening Lofi Girl's livestream")
            webbrowser.open('https://www.youtube.com/watch?v=jfKfPfyJRdk')
            
        elif statement in ("pomodoro timer"):
            print("OK. Opening Pomofocus, a very good pomodoro timer. \
                Add the task you want to focus on, allow notifications \
                and click on START. It should help you focus on your taks.")
            speak("OK. Opening Pomofocus, a very good pomodoro timer. \
                Add the task you want to focus on, allow notifications \
                and click on START. It should help you focus on your taks.")
            webbrowser.open("https://pomofocus.io/")
            
        #elif "help me choose a movie"
        #elif "open netflix"
        #elif "open amazon prime"
        #elif "distraction-free" or "minimize all windows"
        # import wnck
        #screen = wnck.screen_get_default()
        #windows = screen.get_windows()
        #active = screen.get_active_window()
        #for w in windows:
        #    if not w == active:
        #          w.minimize()
        #    
        else:
            print('Unable to read your command\nError: Unknown command')
            speak('Sorry. I wasn\'t able to read your command.\
                  Say Hey Ameli, in case you need anything. \
                  I\'ll always be here for you.')
            time.sleep(2)
            
showmagic()