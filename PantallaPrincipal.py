from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.app import App

class PantallaPrincipal(MDScreen):
    def salir(self,obj): from kivy.app import App; import sys; App.get_running_app().stop(); sys.exit(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(
            orientation="vertical",
            spacing=15,
            padding=20
        )

        titulo = MDLabel(
            text="MiSegundaApp",
            halign="center",
            font_style="H4"
        )

        btn_clientes = MDRaisedButton(text="Clientes", on_release=self.abrir_clientes)
        btn_provincias = MDRaisedButton(text="Provincias")
        btn_cantones = MDRaisedButton(text="Cantones")
        btn_distritos = MDRaisedButton(text="Distritos")
        btn_reportes = MDRaisedButton(text="Reportes")
        btn_estadisticas = MDRaisedButton(text="Estadisticas")
        btn_configuracion = MDRaisedButton(text="Configuracion")
        btn_salir = MDRaisedButton(text="Salir", on_release=self.salir)

        layout.add_widget(titulo)

        layout.add_widget(btn_clientes)
        layout.add_widget(btn_provincias)
        layout.add_widget(btn_cantones)
        layout.add_widget(btn_distritos)
        layout.add_widget(btn_reportes)
        layout.add_widget(btn_estadisticas)
        layout.add_widget(btn_configuracion)
        layout.add_widget(btn_salir)

        self.add_widget(layout)

    def abrir_clientes(self, obj):

        from Clientes import Clientes

        self.clear_widgets()

        self.add_widget(Clientes())
