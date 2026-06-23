from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from PantallaPrincipal import PantallaPrincipal


class PantallaLogin(MDScreen):
    def entrar(self, obj):

        self.clear_widgets()

        self.add_widget(PantallaPrincipal())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            padding=40,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        titulo = MDLabel(
            text="MiSegundaApp",
            halign="center",
            font_style="H4" # o H3
        )

        self.txt_usuario = MDTextField(
            hint_text="Usuario"
        )

        self.txt_clave = MDTextField(
            hint_text="Contrasena",
            password=True
        )

        boton = MDRaisedButton(
            text="Entrar",
            pos_hint={"center_x": 0.5},
            on_release=self.entrar
        )

        layout.add_widget(titulo)
        layout.add_widget(self.txt_usuario)
        layout.add_widget(self.txt_clave)
        layout.add_widget(boton)

        self.add_widget(layout)
