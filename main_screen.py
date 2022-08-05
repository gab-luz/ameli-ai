# Hello, hallo, bonjour, olá!
# Welcome to Ameli, your AI-powered personal voice assistant
# the most complete opensource voice assistant on the internet
# I'm preparing for the first run
# Good things come for those who wait
# Made in Brazil for the world
# https://www.youtube.com/watch?v=Orli-dtFn68
from kivy.core.text import LabelBase
from kivy.uix.image import AsyncImage
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.animation import Animation
Window.size = (350,600)


class AssistantAnimation(AsyncImage):
    Loader.loading_image = 'anim/animation_640_l5ysiybq.gif'

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

class ChangingText(MDApp):
    
    id = 1
    
    def on_start(self):
        self.start()
        
    def start(self, *args):
        anim = Animation(opacity=1, duration=1)
        anim += Animation(opacity=1, duration=3)
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