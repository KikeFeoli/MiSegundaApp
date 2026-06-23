from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from PantallaLogin import PantallaLogin
from kivy.core.window import Window

Window.size = (1600, 1000)  #(1200, 650)
Window.left = -1750
Window.top = 25 # 120

class MiSegundaApp(MDApp):

    def build(self):
        self.title = "MiSegundaApp"
        self.theme_cls.theme_style = "Light"    # "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        return PantallaLogin()   # 👈 aquí está el cambio

MiSegundaApp().run()
