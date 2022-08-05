from sys import platform
from googletts_voice import *
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
from wakeword import background_listening

you = 'Sir'
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

def ameliResponse(audio):
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
    #knick_input_mode= mode_select() # not planning to use text mode on Ameli
    #didn't remove it, just in case
    while True:
        #playsound.playsound(os.path.join('media\sfx',"howcanihelpyounow.mp3"))
        #print("\nTell Me How Can I Help you Now ?")
        ask=any_random(asking)
        print("\n",ask)
        speak(ask+".")
        #statement=take_input(knick_input_mode)
        statement=get_audio().lower()

        if statement==None:
            print("No Input Detected!\n")
            continue
        elif "good bye" in statement or "ok bye" in statement or "stop" in statement or "bye" in statement or "quit" in statement:
            print("\n")
            print('    Your Personal Assistant Knick is Shutting Down,Good bye.     ')
            print("~   The BOT went Offline    ~")
            time.sleep(4)
            cleaner()
            quit()
        
        elif "pause" in statement or "please pause" in statement:
            speak("Assistant Paused.")
            print("ok I am paused\nPress 'W' whenever You Want Me to Resume")
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
                
                # with keyboard.Events() as events:
                #     for event in events:
                #         if event.key == keyboard.Key.w:
                #             speak("Assistant Resumed.")
                #             print(assistant_resumed)
                #             print("  ")
                #             #break
                #               continue
        
        elif "hibernate" in statement or "sleep" in statement: #note this feature only works if there is a mic connected. 
            speak("Hibernating.")
            print("please use the wakeword to wake me up, till then i'll be going undercover.")
            print("Available Wake Words :\n1.Assistant activate\n2.wake up assistant")
            time.sleep(2)
            subprocess.call('start scripts/Hotword/hotword_detection.pyw', shell=True)
            time.sleep(0.5)
            quit() #when this part of the code worked,beleive me... it was cool as Af.

        elif statement in ["no thanks","no","not now","leave me alone"]:
            speak("OK, I will sleep for some time then.")
            print("OK, I will sleep for some time then.")
            print("\nuse the wakeword to awake me, till then I'll be going undercover.")
            time.sleep(2)
            subprocess.call('python wakeword.py', shell=True)
            quit()

        elif "hi"==statement or "hello" in statement :
            hello_greating=any_random(hello)
            print(hello_greating,"\n(NOTE:if you wanna have chat with me. just use the 'Lets Chat' command)")
            speak(hello_greating)
            time.sleep(1)

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
            print("Opening Snipping Tool")
            os.system("start snippingtool")
            time.sleep(5)

        elif "screenshot" in statement:
            import random
            time.sleep(1.5)
            import pyscreenshot
            image = pyscreenshot.grab()
            r = random.randint(1,20000000)
            file_name=("knickscreenshot"+ str(r) +".png")
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
                    print('Ameli is not supported in macOs yet. Sorry.')
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
            pywhatkit.image_to_ascii_art(imgpath=ima,output_file="knick_asciiart.txt")
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
            playsound._playsoundWin(os.path.join('media\sfx',"taskcompleted.mp3"))
            time.sleep(3)

        elif "open my sent mails" in statement or "open my sent mail" in statement:
            webbrowser.open_new_tab("https://mail.google.com/mail/u/0/#sent")
            playsound._playsoundWin(os.path.join('media\sfx',"taskcompleted.mp3"))
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
                print('Not implemented yet')
            print("Command Prompt is Open Now")
            speak("Terminal is open")
            time.sleep(3)

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
                speak("you should press enter if any dialog box appears.")
                time.sleep(1.3)
                speak("Recycle Bin Emptied")
                
        elif "note" in statement or "remember this" in  statement:
                print("What would you like me to write down?")
                speak("What would you like me to write down?")
                note_text = take_input(knick_input_mode)
                note(note_text)
                print("I have made a note of that.\n")

        elif "weather" in statement:
            #API KEY REQUIRED HERE
            if weather_api_key=="YOUR API KEY HERE":   #{this part can be comment out later,and indexing below shall be fixed
                print("You need to get an API key first!\n")
                break
            else:                                      #}
                base_url="https://api.openweathermap.org/data/2.5/weather?"
                playsound._playsoundWin(os.path.join('media\sfx',"cityname.mp3"))
                print("\nwhats the city?")
                city_name= take_input(knick_input_mode)
                complete_url=base_url+"appid="+weather_api_key+"&q="+city_name     #weather_api_key is the api key here
                response = requests.get(complete_url)
                x=response.json()
                if x["cod"]!="404":
                    y=x["main"]
                    current_temperature = y["temp"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    
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
                    speak(" City Not Found. ")
                    print(" City Not Found ")

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
                query=take_input(knick_input_mode)
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
            ameliResponse('wallpaper changed successfully')
            
        # elif 'tell me a joke' in statement:

        #elif 'suggest me a movie' in statement:
            
        elif 'I\'m bored' in statement:
            bored_api = requests.get('https://www.boredapi.com/api/activity', verify=False)
            bored_api_activity = bored_api.json()
            print(bored_api_activity['activity'])
            speak(bored_api_activity['activity'])
        
        elif 'wikipedia' in statement:
            speak("Searching Wikipedia about it...")
            statement =statement.replace("search on wikipedia about", "")
            try:
                results = wikipedia.summary(statement, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except:
                speak("Unknown Error Occured, say your question again.")
                continue
            
        # build a screen recorder here
        
        elif 'who is' in statement:
            try:
                speak("getting information from Wikipedia..")
                statement =statement.replace("who is","")
                results = wikipedia.summary(statement, sentences=3)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except:
                speak("Enable to Fetch Data,try again.")
                continue
        
        elif "what time is it" in statement:
            time_now = datetime.today().strftime("%H:%M %p")
            speak(f"Well, it's {time_now}")
            print("Current Time =", time_now)

        elif 'news for today' in statement or 'tell me the news' in statement or 'read the news please' in statement:
            try:
                news_url="https://news.google.com/news/rss" # you must allow user to choose a different source
                Client=urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"xml")
                news_list=soup_page.findAll("item")
                for news in news_list[:15]:
                    ameliResponse(news.title.text.encode('utf-8'))
            except Exception as e:
                print(e)

        elif 'where is' in  statement:
            ind = statement.split().index("is")
            location = statement[ind + 8:]
            url = "https://www.google.com/maps/place/" + "".join(location)
            speak("This is where i found, " + str(location))
            webbrowser.open(url)    
            
            time.sleep(3)

        elif 'yt studio' in statement or 'open yt studio' in statement or 'open youtube studio' in statement:
            webbrowser.open_new_tab("https://studio.youtube.com/")
            speak("opening youtube creator studio")
            
            time.sleep(5)

        elif 'live studio' in statement or 'livestream dashboard' in statement or 'live control room' in statement:
            webbrowser.open_new_tab('https://studio.youtube.com/channel/UCWe1CSEpVq_u6WDk3F7E2Mg/livestreaming/manage')
            speak("opening youtube livestream dashboard")
            
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

        elif 'viewbot' in statement or 'livebot' in statement or 'view bot' in statement:
            playsound._playsoundWin(os.path.join('media\sfx','startingviewbot.mp3'))
            print("if you get any error in the viewbot or it doesn't work try updating the Assistant or \n vist the official website of knick assistant & check the ViewBot Page.")
            subprocess.call('viewbot\livebot.exe')
            time.sleep(3)
                
        elif 'how were you born' in statement  or 'why were you born' in statement:
            print('''
            I was born on june 2021 by A Boy Who Had an Ambition To Change This World with the
            Help Of Artificial Intelligence, Although i am still just a small step towards this
            new ERA of A.I . But I am still Happy to be Born and serve you right now''')
            time.sleep(3)
        
        elif 'who are you' in statement or 'what can you do' in statement:
            print('I am Knick your Persoanl AI assistant. I am programmed for managing normal tasks in your Life')
            speak("I am Knick your Persoanl AI assistant. I am programmed for managing normal tasks in your Life")
            time.sleep(3)

        elif 'your name' in statement or 'what is your name' in statement :
            speak("my name is knick, how could you forget me :-(")
            print('my name is knick your A.I assistant')
            print(" (ㆆ_ㆆ) "*3)
            time.sleep(3)

        elif 'what is your slogan' in statement or 'what is your motive' in statement:
            playsound._playsoundWin(os.path.join('media\sfx','slogan.mp3'))
            print('Leading Towards A Efficient Life.')
            time.sleep(3)
        
        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by my great all mighty master, Arsh")
            print("I was built by Arsh")
            time.sleep(2)

        elif 'update knick' in statement or 'knick website' in statement:
            speak("opening The Official Website For Knick Assistant.")
            webbrowser.open_new_tab("https://knickassistant.wordpress.com/")
            speak("please manually check for any new Available verson.")
            time.sleep(4)

        elif 'tell commands' in statement or 'your commands' in statement  or 'command' in statement:
            speak("Telling you the list of my commands :")
            speak("below is the list of all commands respectively.")
            print('\n\nbelow is the list of all commands respectively')
            from console import command_list
            print(command_list)
            time.sleep(3)
        
        elif 'chat' in statement: 
            #print('\nChat Feature is Still in ALPHA vesion,\nso please have patience while using it.')
            chat(knick_input_mode)
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
                evil=requests.get(url='https://evilinsult.com/generate_insult.php?lang=en&type=json')
                data=evil.json()
                insult=data['insult']
                print(insult)
                speak(insult)
                time.sleep(2)
            except:
                print("the insult generation server is down,you may try again later.")
                speak("I'm afraid I can't do it right now. Maybe... another time?")

        elif 'i want to dictate' in statement:
            speak("okay opening dictation option.")
            time.sleep(0.5)
            keyboard.press_and_release('win+H')
            time.sleep(0.5)
            playsound._playsoundWin(os.path.join('media\sfx','done.wav'))
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
            
        elif statement in {"depressed","I'm depressed","I\'m very depressed"}:
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
                    playsound._playsoundWin(os.path.join('media\sfx',"taskcompleted.mp3"))
                    time.sleep(5)
                else:
                    speak("Oh, I see. Please get some help. Okay?")
            elif "no" in depressed_audio:
                speak('Oh, I see. Please get some help. Okay?')
            time.sleep(2)
            

        elif "support assistance" in statement:
            speak("you can join the official discord server of knick, if you have any problem while using the assistant.")
            query=input("do you want to join the Discord Server for Assistance? (y/n)\n>> ")
            if query=="y":
                webbrowser.open_new_tab("https://discord.gg/2X4WThB64b")
                continue
            elif query=="n":
                print("ok : action cancelled by user")
                continue
            else:
                print("you need to select from 'y' or 'n' only, IDOT!")
                continue
        
        elif statement in ["focus","help me focus please","I can\t focus"]:
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
            print('Unable to Read Your Command\nError: Unknown Command')
            speak('Sorry. I wasn\'t able to read your command.\
                  Say Hey Ameli in case you need anything. \
                  I\'ll always be here for you.')
            time.sleep(2)
            
showmagic()