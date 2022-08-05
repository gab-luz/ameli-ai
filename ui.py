#import kivy
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRectangleFlatButton
# kivy:
from kivy.app import App
from kivy.lang import Builder

# our animation:
# https://lottiefiles.com/7227-vui-animation by Aneesh Ravi 
# 


GUI = Builder.load_file('main.kv')

class MainApp(App):
    
    def build(self): # build function is used to allow us to construct/build our app
        return GUI

MainApp().run()

# we're going to use KivyMD after using Kivy
# class MainApp(MDApp):
#     def build(self):
#         screen = Screen()
#         screen.add_widget(
#             MDRectangleFlatButton(
#                 text="Hello, User...",
#                 pos_hint={"center_x": 0.5, "center_y": 0.5},
#             )
#         )
#         #screen.MDLabel(text="Hello, World", halign="center")
#         return screen