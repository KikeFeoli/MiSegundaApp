from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from Conexion import Conectar
from datetime import datetime
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

class Clientes(MDScreen):
    # CONFIGURACIÓN DE COLUMNAS (size_hint_x distribuido correctamente)
    COLUMNAS = {
        "Id": 0.06,
        "Nombre": 0.16,
        "Apellido1": 0.16,
        "Apellido2": 0.16,
        "Fecha": 0.14,
        "Provincia": 0.16,
        "Canton": 0.10,
        "Distrito": 0.10
    }
    
    def crear_tabla_clientes(self):
        self.scroll_clientes = ScrollView(size_hint=(1, 1))
        self.tabla_clientes = MDGridLayout(cols=1, spacing=1, size_hint_y=None)
        self.tabla_clientes.bind(minimum_height=self.tabla_clientes.setter("height"))
        self.scroll_clientes.add_widget(self.tabla_clientes)
        self.ids.contenedor_clientes.clear_widgets()
        self.ids.contenedor_clientes.add_widget(self.scroll_clientes)
        self.crear_encabezado()

    def crear_encabezado(self):
        """Crea el encabezado de la tabla con botones ordenables."""
        fila = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(45), spacing=5)
        
        for nombre_columna in self.COLUMNAS.keys():
            btn = MDRaisedButton(
                text=nombre_columna,
                size_hint_x=self.COLUMNAS[nombre_columna],
                font_size="10sp",
                md_bg_color=(0.4, 0.5, 0.55, 1),
                on_release=lambda x, col=nombre_columna: self.ordenar(col)
            )
            fila.add_widget(btn)
        
        self.tabla_clientes.add_widget(fila)

    def mostrar_clientes(self):
        """Muestra los clientes en la tabla."""
        self.tabla_clientes.clear_widgets()
        self.crear_encabezado()
        self.botones_id = []
        
        for i, fila in enumerate(self.clientes_encontrados):
            id_cliente = fila[0]
            fecha = datetime.strptime(str(fila[4]), "%Y-%m-%d").strftime("%d-%m-%Y") if fila[4] else ""
            provincia = "" if fila[5] is None else str(fila[5])
            canton = "" if fila[6] is None else str(fila[6])
            distrito = "" if fila[7] is None else str(fila[7])
            
            # Colores alternados para mejor legibilidad
            color = (1, 1, 1, 1) if i % 2 == 0 else (0.93, 0.93, 0.93, 1)
            fila_tabla = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(42), spacing=5, md_bg_color=color)
            
            # Botón ID (seleccionable)
            btn = MDRaisedButton(
                text=str(id_cliente),
                size_hint_x=self.COLUMNAS["Id"],
                font_size="10sp",
                md_bg_color=(0.4, 0.5, 0.55, 1)
            )
            btn.bind(on_release=lambda x, idc=id_cliente, b=btn: self.seleccionar_cliente(idc, b))
            self.botones_id.append(btn)
            fila_tabla.add_widget(btn)
            
            # Labels con datos (usando mismas proporciones que el encabezado)
            fila_tabla.add_widget(MDLabel(text=str(fila[1]), font_size="12sp", halign="left", size_hint_x=self.COLUMNAS["Nombre"]))
            fila_tabla.add_widget(MDLabel(text=str(fila[2]), font_size="12sp", halign="left", size_hint_x=self.COLUMNAS["Apellido1"]))
            fila_tabla.add_widget(MDLabel(text=str(fila[3]), font_size="12sp", halign="left", size_hint_x=self.COLUMNAS["Apellido2"]))
            fila_tabla.add_widget(MDLabel(text=fecha, font_size="12sp", halign="center", size_hint_x=self.COLUMNAS["Fecha"]))
            fila_tabla.add_widget(MDLabel(text=provincia, font_size="12sp", halign="left", size_hint_x=self.COLUMNAS["Provincia"]))
            fila_tabla.add_widget(MDLabel(text=canton, font_size="12sp", halign="left", size_hint_x=self.COLUMNAS["Canton"]))
            fila_tabla.add_widget(MDLabel(text=distrito, font_size="12sp", halign="left", size_hint_x=self.COLUMNAS["Distrito"]))
            
            self.tabla_clientes.add_widget(fila_tabla)

    # ================= CRUD =================
    
    def seleccionar_cliente(self, id_cliente, btn):
        """Selecciona un cliente desde la tabla."""
        if self.btnSeleccionado:
            self.btnSeleccionado.md_bg_color = (0.4, 0.5, 0.55, 1)
        btn.md_bg_color = (0.1, 0.5, 1, 1)
        self.btnSeleccionado = btn
        
        for cliente in self.clientes_encontrados:
            if int(cliente[0]) == int(id_cliente):
                self.idCliente = cliente[0]
                self.txtNombre.text = str(cliente[1]) if cliente[1] else ""
                self.txtApellido1.text = str(cliente[2]) if cliente[2] else ""
                self.txtApellido2.text = str(cliente[3]) if cliente[3] else ""
                self.txtFechaNacimiento.text = datetime.strptime(str(cliente[4]), "%Y-%m-%d").strftime("%d-%m-%Y") if cliente[4] else ""
                self.cmbProvincia.text = str(cliente[5]) if cliente[5] else ""
                self.cmbCanton.text = str(cliente[6]) if cliente[6] else ""
                self.cmbDistrito.text = str(cliente[7]) if cliente[7] else ""
                break

    def modificar_cliente(self):
        """Modifica el cliente seleccionado."""
        if self.idCliente == 0:
            toast("Seleccione un cliente")
            return
        try:
            conexion = Conectar()
            cursor = conexion.cursor()
            fecha = self.txtFechaNacimiento.text.strip()
            
            if "-" in fecha and len(fecha) == 10 and fecha[2] == "-":
                fecha_sql = datetime.strptime(fecha, "%d-%m-%Y").strftime("%Y-%m-%d")
            else:
                fecha_sql = fecha
            
            cursor.execute(
                "UPDATE Clientes SET Nombre=?, Apellido1=?, Apellido2=?, FechaNacimiento=?, idProvincia=?, idCanton=?, idDistrito=? WHERE Id=?",
                (self.txtNombre.text.strip().upper(), self.txtApellido1.text.strip().upper(), 
                 self.txtApellido2.text.strip().upper(), fecha_sql, self.idProvincia, self.idCanton, 
                 self.idDistrito, self.idCliente)
            )
            conexion.commit()
            conexion.close()
            self.cargar_datos()
            toast("Cliente modificado")
        except Exception as error:
            toast(str(error))

    def eliminar_cliente(self):
        """Elimina el cliente seleccionado."""
        if self.idCliente == 0:
            toast("Seleccione un cliente")
            return
        try:
            conexion = Conectar()
            cursor = conexion.cursor()
            sql = "DELETE FROM Clientes WHERE Id=?"
            cursor.execute(sql, self.idCliente)
            conexion.commit()
            conexion.close()
            toast("Cliente eliminado")
            self.cargar_datos()
            self.nuevo(None)
        except Exception as error:
            toast(str(error))

    def confirmar_eliminar(self):
        """Muestra diálogo de confirmación para eliminar."""
        self.dialog = MDDialog(
            title="Confirmación",
            text="¿Desea eliminar este cliente?",
            buttons=[
                MDRaisedButton(text="Cancelar", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="Eliminar", on_release=lambda x: self.ejecutar_eliminar())
            ]
        )
        self.dialog.open()

    def ejecutar_eliminar(self, *args):
        """Ejecuta la eliminación del cliente."""
        self.dialog.dismiss()
        self.eliminar_cliente()

    def nuevo(self, obj):
        """Limpia los campos para un nuevo registro."""
        self.idCliente = 0
        self.idProvincia = 0
        self.idCanton = 0
        self.idDistrito = 0
        self.txtNombre.text = ""
        self.txtApellido1.text = ""
        self.txtApellido2.text = ""
        self.txtFechaNacimiento.text = ""
        self.cmbProvincia.text = "Seleccione Provincia"
        self.cmbCanton.text = "Seleccione Canton"
        self.cmbDistrito.text = "Seleccione Distrito"
        self.cargar_datos()
        self.cargar_provincias()
        self.txtNombre.focus = True

    # ================= BASE DE DATOS =================
    
    def registrar(self, obj):
        """Registra un nuevo cliente."""
        nombre = self.txtNombre.text.strip().upper()
        apellido1 = self.txtApellido1.text.strip().upper()
        apellido2 = self.txtApellido2.text.strip().upper()
        fechaNacimiento = self.txtFechaNacimiento.text.strip()
        
        # Validaciones
        if nombre == "":
            toast("Debe digitar el nombre")
            return
        if apellido1 == "":
            toast("Debe digitar Apellido1")
            return
        if apellido2 == "":
            toast("Debe digitar Apellido2")
            return
        if fechaNacimiento == "":
            toast("Debe digitar la fecha")
            return
        if self.idProvincia == 0:
            toast("Seleccione Provincia")
            return
        if self.idCanton == 0:
            toast("Seleccione Canton")
            return
        if self.idDistrito == 0:
            toast("Seleccione Distrito")
            return
        
        try:
            datetime.strptime(fechaNacimiento, "%d-%m-%Y")
        except:
            toast("Fecha inválida (formato: dd-mm-yyyy)")
            return
        
        try:
            conexion = Conectar()
            cursor = conexion.cursor()
            fecha_sql = datetime.strptime(fechaNacimiento, "%d-%m-%Y").strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO Clientes (Nombre, Apellido1, Apellido2, FechaNacimiento, IdProvincia, IdCanton, IdDistrito) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (nombre, apellido1, apellido2, fecha_sql, self.idProvincia, self.idCanton, self.idDistrito)
            )
            conexion.commit()
            conexion.close()
            self.cargar_datos()
            self.nuevo(None)
            toast("Cliente registrado")
        except Exception as error:
            toast(str(error))

    def cargar_datos(self):
        """Carga todos los clientes de la BD."""
        try:
            conexion = Conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT C.Id, C.Nombre, C.Apellido1, C.Apellido2, C.FechaNacimiento, 
                       P.NombreProvincia, CA.NombreCanton, D.NombreDistrito 
                FROM Clientes C 
                LEFT JOIN Provincias P ON C.IdProvincia = P.IdProvincia 
                LEFT JOIN Cantones CA ON C.IdCanton = CA.IdCanton 
                LEFT JOIN Distritos D ON C.IdDistrito = D.IdDistrito 
                ORDER BY C.Id
            """)
            datos = cursor.fetchall()
            conexion.close()
            self.clientes_encontrados = datos
            self.mostrar_clientes()
        except Exception as error:
            toast(str(error))

    def buscar(self, obj):
        """Busca clientes por nombre o apellido."""
        nombre = self.txtNombre.text.strip().upper()
        apellido1 = self.txtApellido1.text.strip().upper()
        apellido2 = self.txtApellido2.text.strip().upper()
        
        if nombre == "" and apellido1 == "" and apellido2 == "":
            toast("Digite al menos un criterio")
            self.txtNombre.focus = True
            return
        
        try:
            conexion = Conectar()
            cursor = conexion.cursor()
            sql = """
                SELECT C.Id, C.Nombre, C.Apellido1, C.Apellido2, C.FechaNacimiento, 
                       P.NombreProvincia, CA.NombreCanton, D.NombreDistrito 
                FROM Clientes C 
                LEFT JOIN Provincias P ON C.IdProvincia = P.IdProvincia 
                LEFT JOIN Cantones CA ON C.IdCanton = CA.IdCanton 
                LEFT JOIN Distritos D ON C.IdDistrito = D.IdDistrito 
                WHERE 1=1
            """
            parametros = []
            
            if nombre != "":
                sql += " AND C.Nombre LIKE ?"
                parametros.append("%" + nombre + "%")
            if apellido1 != "":
                sql += " AND C.Apellido1 LIKE ?"
                parametros.append("%" + apellido1 + "%")
            if apellido2 != "":
                sql += " AND C.Apellido2 LIKE ?"
                parametros.append("%" + apellido2 + "%")
            
            cursor.execute(sql, parametros)
            datos = cursor.fetchall()
            conexion.close()
            
            self.clientes_encontrados = datos
            self.mostrar_clientes()
            
            if len(datos) == 0:
                toast("No existen registros")
                self.txtNombre.focus = True
        except Exception as error:
            toast(str(error))

    def ordenar(self, columna):
        """Ordena la tabla por la columna seleccionada (ascendente/descendente)."""
        # Diccionario de índices de columnas
        indices = {
            "Id": 0,
            "Nombre": 1,
            "Apellido1": 2,
            "Apellido2": 3,
            "Fecha": 4,
            "Provincia": 5,
            "Canton": 6,
            "Distrito": 7
        }
        
        # Cambiar dirección si es la misma columna
        if self.columna_orden == columna:
            self.ascendente = not self.ascendente
        else:
            self.ascendente = True
        
        self.columna_orden = columna
        indice = indices[columna]
        
        # Ordenar la lista
        self.clientes_encontrados = sorted(
            self.clientes_encontrados,
            key=lambda x: str(x[indice]).upper() if x[indice] is not None else "",
            reverse=not self.ascendente
        )
        
        self.mostrar_clientes()

    # ================= PROVINCIAS, CANTONES, DISTRITOS =================
    
    def cargar_provincias(self):
        """Carga las provincias de la BD."""
        conexion = Conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT IdProvincia, NombreProvincia FROM Provincias ORDER BY NombreProvincia")
        datos = cursor.fetchall()
        conexion.close()
        
        self.provincias = {}
        for fila in datos:
            self.provincias[fila[1]] = fila[0]

    def cargar_cantones(self, idProvincia):
        """Carga los cantones según la provincia seleccionada."""
        conexion = Conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT IdCanton, NombreCanton FROM Cantones WHERE IdProvincia=? ORDER BY NombreCanton", (idProvincia,))
        datos = cursor.fetchall()
        conexion.close()
        
        self.cantones = {}
        for fila in datos:
            self.cantones[fila[1]] = fila[0]

    def cargar_distritos(self, idCanton):
        """Carga los distritos según el cantón seleccionado."""
        conexion = Conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT IdDistrito, NombreDistrito FROM Distritos WHERE IdCanton=? ORDER BY NombreDistrito", (idCanton,))
        datos = cursor.fetchall()
        conexion.close()
        
        self.distritos = {}
        for fila in datos:
            self.distritos[fila[1]] = fila[0]

    def seleccionar_provincia(self, nombre):
        """Evento al seleccionar provincia."""
        self.cmbProvincia.text = nombre
        self.idProvincia = self.provincias[nombre]
        self.menuProvincia.dismiss()
        self.cargar_cantones(self.idProvincia)
        
        items = []
        for nombreCanton in self.cantones:
            items.append({"text": nombreCanton, "on_release": lambda x=nombreCanton: self.seleccionar_canton(x)})
        
        self.menuCanton.dismiss()
        self.menuCanton = MDDropdownMenu(caller=self.cmbCanton, items=items, width_mult=4)

    def seleccionar_canton(self, nombre):
        """Evento al seleccionar cantón."""
        self.cmbCanton.text = nombre
        self.idCanton = self.cantones[nombre]
        self.menuCanton.dismiss()
        self.cargar_distritos(self.idCanton)
        
        items = []
        for nombreDistrito in self.distritos:
            items.append({"text": nombreDistrito, "on_release": lambda x=nombreDistrito: self.seleccionar_distrito(x)})
        
        self.menuDistrito.dismiss()
        self.menuDistrito = MDDropdownMenu(caller=self.cmbDistrito, items=items, width_mult=4)

    def seleccionar_distrito(self, nombre):
        """Evento al seleccionar distrito."""
        self.cmbDistrito.text = nombre
        self.idDistrito = self.distritos[nombre]
        self.menuDistrito.dismiss()

    def regresar(self, obj):
        """Regresa a la pantalla principal."""
        from PantallaPrincipal import PantallaPrincipal
        self.clear_widgets()
        self.add_widget(PantallaPrincipal())

    # ================= INICIALIZACIÓN =================
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Inicializar variables
        self.botones_id = []
        self.clientes_encontrados = []
        self.idCliente = 0
        self.btnSeleccionado = None
        self.idProvincia = 0
        self.idCanton = 0
        self.idDistrito = 0
        self.provincias = {}
        self.cantones = {}
        self.distritos = {}
        self.columna_orden = "Id"
        self.ascendente = True
        
        # Crear interfaz
        scroll = ScrollView(size_hint=(1, 1))
        layout = MDGridLayout(cols=1, spacing=8, padding=[25, 15, 25, 15], size_hint=(1, None))
        layout.bind(minimum_height=layout.setter("height"))
        
        # Título
        titulo = MDLabel(text="Clientes", halign="center", font_style="H4", size_hint_y=None, height=50)
        
        # Campos de entrada
        self.txtNombre = MDTextField(hint_text="Nombre", size_hint_y=None, height=60)
        self.txtApellido1 = MDTextField(hint_text="Apellido1", size_hint_y=None, height=60)
        self.txtApellido2 = MDTextField(hint_text="Apellido2", size_hint_y=None, height=60)
        self.txtFechaNacimiento = MDTextField(hint_text="dd-mm-yyyy", size_hint_y=None, height=60)
        
        # Combos (Provincia, Cantón, Distrito)
        self.cmbProvincia = MDRaisedButton(text="Seleccione Provincia", size_hint=(None, None), width=250, height=45, pos_hint={"center_x": 0.5})
        self.cmbCanton = MDRaisedButton(text="Seleccione Canton", size_hint=(None, None), width=250, height=45, pos_hint={"center_x": 0.5})
        self.cmbDistrito = MDRaisedButton(text="Seleccione Distrito", size_hint=(None, None), width=250, height=45, pos_hint={"center_x": 0.5})
        
        # Filas para combos
        filaProvincia = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        filaProvincia.add_widget(MDLabel())
        filaProvincia.add_widget(self.cmbProvincia)
        filaProvincia.add_widget(MDLabel())
        
        filaCanton = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        filaCanton.add_widget(MDLabel())
        filaCanton.add_widget(self.cmbCanton)
        filaCanton.add_widget(MDLabel())
        
        filaDistrito = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        filaDistrito.add_widget(MDLabel())
        filaDistrito.add_widget(self.cmbDistrito)
        filaDistrito.add_widget(MDLabel())
        
        # Botones
        fila_botones = MDBoxLayout(size_hint_y=None, height=55, spacing=10, adaptive_width=True, pos_hint={"center_x": 0.5})
        
        self.btnNuevo = MDRaisedButton(text="Nuevo", on_release=self.nuevo)
        self.btnRegistrar = MDRaisedButton(text="Registrar", on_release=self.registrar)
        self.btnBuscar = MDRaisedButton(text="Buscar", on_release=self.buscar)
        self.btnModificar = MDRaisedButton(text="Modificar", on_release=lambda x: self.modificar_cliente())
        self.btnEliminar = MDRaisedButton(text="Eliminar", on_release=lambda x: self.confirmar_eliminar())
        self.btnRegresar = MDRaisedButton(text="Regresar", on_release=self.regresar)
        
        fila_botones.add_widget(self.btnNuevo)
        fila_botones.add_widget(self.btnRegresar)
        fila_botones.add_widget(self.btnRegistrar)
        fila_botones.add_widget(self.btnBuscar)
        fila_botones.add_widget(self.btnModificar)
        fila_botones.add_widget(self.btnEliminar)
        
        # Tabla
        self.scroll_clientes = ScrollView(size_hint=(1, None), height=340, do_scroll_x=True, do_scroll_y=True)
        self.tabla_clientes = MDGridLayout(cols=1, spacing=1, size_hint=(None, None), width=1450)
        self.tabla_clientes.pos_hint = {"center_x": 0.5}
        self.tabla_clientes.bind(minimum_height=self.tabla_clientes.setter("height"))
        self.scroll_clientes.add_widget(self.tabla_clientes)
        
        # Agregar widgets al layout
        layout.add_widget(titulo)
        layout.add_widget(self.txtNombre)
        layout.add_widget(self.txtApellido1)
        layout.add_widget(self.txtApellido2)
        layout.add_widget(self.txtFechaNacimiento)
        layout.add_widget(filaProvincia)
        layout.add_widget(filaCanton)
        layout.add_widget(filaDistrito)
        layout.add_widget(fila_botones)
        layout.add_widget(self.scroll_clientes)
        
        scroll.add_widget(layout)
        self.add_widget(scroll)
        
        # Cargar datos iniciales
        self.cargar_datos()
        self.cargar_provincias()
        
        # Menús dropdown
        items = []
        for nombre in self.provincias:
            items.append({"text": nombre, "on_release": lambda x=nombre: self.seleccionar_provincia(x)})
        
        self.menuProvincia = MDDropdownMenu(caller=self.cmbProvincia, items=items, width_mult=4)
        self.menuCanton = MDDropdownMenu(caller=self.cmbCanton, items=[], width_mult=4)
        self.menuDistrito = MDDropdownMenu(caller=self.cmbDistrito, items=[], width_mult=4)
        
        self.cmbProvincia.bind(on_release=lambda x: self.menuProvincia.open())
        self.cmbCanton.bind(on_release=lambda x: self.menuCanton.open())
        self.cmbDistrito.bind(on_release=lambda x: self.menuDistrito.open())
