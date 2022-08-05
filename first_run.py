# Hello, hallo, bonjour, olá!
# Welcome to Ameli, your AI-powered personal voice assistant
# the most complete opensource voice assistant on the internet
# I'm preparing for the first run
# Good things come for those who wait
# Made in Brazil for the world
# https://www.youtube.com/watch?v=Orli-dtFn68
from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.animation import Animation
Window.size = (350,600)

# first_run.py will only run if there's no userdata.db available on the app root

kv = '''
MDFloatLayout:
    md_bg_color: 1, 1, 1, 1
    MDLabel:
        id: text1
        text: "Olá"
        halign: "center"
        font_name: "BPoppins"
        font_size: "40sp"
        opacity: 1
    MDLabel:
        id: text2
        text: "Hola"
        halign: "center"
        font_name: "BPoppins"
        font_size: "40sp"
        opacity: 0
    MDLabel:
        id: text3
        text: "Hello"
        halign: "center"
        font_name: "BPoppins"
        font_size: "40sp"
        opacity: 0
    MDLabel:
        id: text4
        text: "Hallo"
        halign: "center"
        font_name: "BPoppins"
        font_size: "40sp"
        opacity: 0
    MDLabel:
        id: text5
        text: "привет"
        halign: "center"
        font_name: "BPoppins"
        font_size: "40sp"
        opacity: 0
    MDLabel:
        id: text6
        text: "你好"
        halign: "center"
        font_name: "BPoppins"
        font_size: "40sp"
        opacity: 0
    MDLabel:
        id: text7
        text: "We're setting up everything for you."
        halign: "center"
        font_name: "BPoppins"
        font_size: "40sp"
        opacity: 0
    MDLabel:
        id: text7
        text: "Done. Now let's ask a few things about you before we can get started."
        halign: "center"
        font_name: "BPoppins"
        font_size: "40sp"
        opacity: 0
'''

#class tellmeAboutYou(MDApp):
# that class will ask a few things about the user
# and store it inside userdata.db
# all the questions will be displayed in text
# and they will also will be prerecorded using
# coqiAI
# "How do you want us to call you?"
# "Are you a boy or a girl?"
# "How old are you?"
# "Do you have a disability that it's important for me to know?"
#    def build(self):
#        return Builder.load_string(kv)

class ChangingText(MDApp):
    
    id = 1
    
    def on_start(self):
        self.start()
        
    def start(self, *args):
        anim = Animation(opacity=1, duration=1)
        anim += Animation(opacity=1, duration=1)
        anim += Animation(opacity=0, duration=1)
        anim.bind(on_complete=self.start)
        anim.start(self.root.ids[f"text{self.id}"])
        if self.id < 7:
            self.id += 1
        
        else:
            self.id -=3
    
    def build(self):
        return Builder.load_string(kv)

if __name__ == '__main__':
    LabelBase.register(
        name='BPoppins',
        fn_regular='/home/mestre/.local/share/fonts/PoppinsLatin-SemiBold.ttf'
    )
    
    ChangingText().run()