
# ==========================================================
# UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA - UNAD
# Proyecto: Sistema Integral de Gestion Software FJ
# Fase 4 - Componente practico
# Archivo: interfaz.py
# Descripcion: Interfaz grafica para clientes, servicios
# y reservas.
# ==========================================================

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from entidades import Cliente

from servicios import (
    ServicioSala,
    ServicioEquipo,
    ServicioAsesoria
)

from reservas import GestorReservas

from excepciones import (
    ErrorValidacion,
    ErrorCliente,
    ErrorServicio,
    ErrorReserva
)

from logs import RegistroSistema


class AplicacionSoftwareFJ:

    def __init__(self, ventana):

        self.ventana = ventana
        self.ventana.title("Software FJ | Sistema de Gestion")
        self.ventana.geometry("1100x750")
        self.ventana.minsize(850, 600)
        self.ventana.configure(bg="#F2F6FC")

        self.clientes = []
        self.servicios = []
        self.gestor = GestorReservas()

        self.contador_cliente = 1
        self.contador_servicio = 1
        self.contador_reserva = 1

        self.configurar_estilos()
        self.crear_ventana_desplazable()
        self.crear_interfaz()
        self.cargar_servicios_iniciales()

    # ======================================================
    # ESTILOS
    # ======================================================

    def configurar_estilos(self):

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TNotebook",
            background="#F2F6FC",
            borderwidth=0
        )

        estilo.configure(
            "TNotebook.Tab",
            background="#DCE7F5",
            foreground="#17365D",
            padding=(22, 12),
            font=("Segoe UI", 10, "bold")
        )

        estilo.map(
            "TNotebook.Tab",
            background=[("selected", "#FFFFFF")],
            foreground=[("selected", "#1769AA")]
        )

        estilo.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#263445",
            rowheight=32,
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Treeview.Heading",
            background="#17365D",
            foreground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            padding=8
        )

        estilo.map(
            "Treeview",
            background=[("selected", "#D5E8FF")],
            foreground=[("selected", "#17365D")]
        )

        estilo.configure(
            "TCombobox",
            padding=7,
            font=("Segoe UI", 10)
        )

    # ======================================================
    # VENTANA DESPLAZABLE
    # ======================================================

    def crear_ventana_desplazable(self):

        contenedor = tk.Frame(
            self.ventana,
            bg="#F2F6FC"
        )

        contenedor.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            contenedor,
            bg="#F2F6FC",
            highlightthickness=0
        )

        self.barra_general = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.barra_general.set
        )

        self.barra_general.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.contenido = tk.Frame(
            self.canvas,
            bg="#F2F6FC"
        )

        self.ventana_canvas = self.canvas.create_window(
            (0, 0),
            window=self.contenido,
            anchor="nw"
        )

        self.contenido.bind(
            "<Configure>",
            self.actualizar_area_desplazamiento
        )

        self.canvas.bind(
            "<Configure>",
            self.ajustar_ancho_contenido
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.desplazar_con_mouse
        )

    def actualizar_area_desplazamiento(self, evento=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def ajustar_ancho_contenido(self, evento):

        self.canvas.itemconfig(
            self.ventana_canvas,
            width=evento.width
        )

    def desplazar_con_mouse(self, evento):

        self.canvas.yview_scroll(
            int(-1 * (evento.delta / 120)),
            "units"
        )

    # ======================================================
    # INTERFAZ PRINCIPAL
    # ======================================================

    def crear_interfaz(self):

        encabezado = tk.Frame(
            self.contenido,
            bg="#17365D",
            height=105
        )

        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="SOFTWARE FJ",
            bg="#17365D",
            fg="white",
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w", padx=30, pady=(18, 0))

        tk.Label(
            encabezado,
            text="Sistema Integral de Gestion de Clientes, Servicios y Reservas",
            bg="#17365D",
            fg="#C9DDF5",
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=32)

        resumen = tk.Frame(
            self.contenido,
            bg="#F2F6FC"
        )

        resumen.pack(fill="x", padx=25, pady=18)

        self.tarjeta_clientes = self.crear_tarjeta(
            resumen, "CLIENTES", "0", "#2471A3"
        )

        self.tarjeta_servicios = self.crear_tarjeta(
            resumen, "SERVICIOS", "0", "#188977"
        )

        self.tarjeta_reservas = self.crear_tarjeta(
            resumen, "RESERVAS", "0", "#7952A0"
        )

        self.pestanas = ttk.Notebook(
            self.contenido,
            height=650
        )

        self.pestanas.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        self.pagina_clientes = tk.Frame(
            self.pestanas,
            bg="white"
        )

        self.pagina_servicios = tk.Frame(
            self.pestanas,
            bg="white"
        )

        self.pagina_reservas = tk.Frame(
            self.pestanas,
            bg="white"
        )

        self.pestanas.add(
            self.pagina_clientes,
            text="  Clientes  "
        )

        self.pestanas.add(
            self.pagina_servicios,
            text="  Servicios  "
        )

        self.pestanas.add(
            self.pagina_reservas,
            text="  Reservas  "
        )

        self.crear_pagina_clientes()
        self.crear_pagina_servicios()
        self.crear_pagina_reservas()

        tk.Label(
            self.contenido,
            text="Software FJ | Proyecto academico UNAD | Python",
            bg="#F2F6FC",
            fg="#708090",
            font=("Segoe UI", 8)
        ).pack(pady=(0, 12))

    # ======================================================
    # TARJETAS DE RESUMEN
    # ======================================================

    def crear_tarjeta(self, padre, titulo, valor, color):

        tarjeta = tk.Frame(
            padre,
            bg="white",
            highlightbackground="#DFE7F1",
            highlightthickness=1
        )

        tarjeta.pack(
            side="left",
            fill="x",
            expand=True,
            padx=7
        )

        tk.Label(
            tarjeta,
            text=titulo,
            bg="white",
            fg="#718096",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=18, pady=(12, 2))

        etiqueta = tk.Label(
            tarjeta,
            text=valor,
            bg="white",
            fg=color,
            font=("Segoe UI", 22, "bold")
        )

        etiqueta.pack(anchor="w", padx=18, pady=(0, 12))

        return etiqueta

    def actualizar_resumen(self):

        self.tarjeta_clientes.config(
            text=str(len(self.clientes))
        )

        self.tarjeta_servicios.config(
            text=str(len(self.servicios))
        )

        self.tarjeta_reservas.config(
            text=str(len(self.gestor.listar_reservas()))
        )

    # ======================================================
    # ELEMENTOS VISUALES
    # ======================================================

    def titulo_seccion(self, padre, titulo, descripcion):

        tk.Label(
            padre,
            text=titulo,
            bg="white",
            fg="#17365D",
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=25, pady=(20, 2))

        tk.Label(
            padre,
            text=descripcion,
            bg="white",
            fg="#718096",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=27, pady=(0, 15))

    def crear_campo(self, padre, texto, fila, columna=0):

        tk.Label(
            padre,
            text=texto,
            bg="white",
            fg="#34495E",
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=fila,
            column=columna,
            sticky="w",
            padx=8,
            pady=(8, 3)
        )

        entrada = tk.Entry(
            padre,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#DCE5EF",
            highlightcolor="#2471A3"
        )

        entrada.grid(
            row=fila + 1,
            column=columna,
            sticky="ew",
            padx=8,
            pady=(0, 7),
            ipady=6
        )

        return entrada

    def crear_boton(self, padre, texto, comando, color="#1769AA"):

        return tk.Button(
            padre,
            text=texto,
            command=comando,
            bg=color,
            fg="white",
            activebackground="#12558A",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=9
        )

    # ======================================================
    # TABLAS
    # ======================================================

    def crear_tabla(
        self,
        padre,
        columnas,
        encabezados,
        anchos,
        altura=8
    ):

        contenedor = tk.Frame(
            padre,
            bg="white"
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings",
            height=altura
        )

        for columna, texto in encabezados.items():

            tabla.heading(
                columna,
                text=texto
            )

        for columna, ancho in anchos.items():

            tabla.column(
                columna,
                width=ancho,
                minwidth=60
            )

        barra_vertical = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=tabla.yview
        )

        barra_horizontal = ttk.Scrollbar(
            contenedor,
            orient="horizontal",
            command=tabla.xview
        )

        tabla.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set
        )

        tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        barra_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        return tabla

    # ======================================================
    # CLIENTES
    # ======================================================

    def crear_pagina_clientes(self):

        self.titulo_seccion(
            self.pagina_clientes,
            "Gestion de clientes",
            "Registra nuevos clientes y consulta su informacion."
        )

        formulario = tk.Frame(
            self.pagina_clientes,
            bg="white"
        )

        formulario.pack(fill="x", padx=20)

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        self.nombre_cliente = self.crear_campo(
            formulario, "Nombre completo", 0, 0
        )

        self.documento_cliente = self.crear_campo(
            formulario, "Documento", 0, 1
        )

        self.correo_cliente = self.crear_campo(
            formulario, "Correo electronico", 2, 0
        )

        self.telefono_cliente = self.crear_campo(
            formulario, "Telefono", 2, 1
        )

        self.crear_boton(
            self.pagina_clientes,
            "+ Registrar cliente",
            self.registrar_cliente
        ).pack(anchor="e", padx=30, pady=12)

        tk.Label(
            self.pagina_clientes,
            text="CLIENTES REGISTRADOS",
            bg="white",
            fg="#17365D",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=28, pady=(8, 5))

        self.tabla_clientes = self.crear_tabla(
            self.pagina_clientes,
            ("id", "nombre", "documento", "correo", "telefono"),
            {
                "id": "ID",
                "nombre": "Nombre",
                "documento": "Documento",
                "correo": "Correo",
                "telefono": "Telefono"
            },
            {
                "id": 65,
                "nombre": 170,
                "documento": 110,
                "correo": 190,
                "telefono": 110
            },
            altura=8
        )

    def registrar_cliente(self):

        try:

            nombre = self.nombre_cliente.get().strip()
            documento = self.documento_cliente.get().strip()
            correo = self.correo_cliente.get().strip()
            telefono = self.telefono_cliente.get().strip()

            if not all([nombre, documento, correo, telefono]):
                raise ErrorValidacion(
                    "Todos los campos son obligatorios."
                )

            for cliente_existente in self.clientes:

                if cliente_existente.documento == documento:
                    raise ErrorCliente(
                        "Ya existe un cliente con ese documento."
                    )

            cliente = Cliente(
                f"C{self.contador_cliente:03d}",
                nombre,
                documento,
                correo,
                telefono
            )

            self.clientes.append(cliente)
            self.contador_cliente += 1

            self.tabla_clientes.insert(
                "",
                "end",
                values=(
                    cliente.identificador,
                    cliente.nombre,
                    cliente.documento,
                    cliente.correo,
                    cliente.telefono
                )
            )

            self.limpiar_campos_cliente()
            self.actualizar_lista_clientes()
            self.actualizar_resumen()

            messagebox.showinfo(
                "Registro exitoso",
                "El cliente fue registrado correctamente."
            )

        except (ErrorValidacion, ErrorCliente) as error:

            messagebox.showerror(
                "Error de registro",
                str(error)
            )

            RegistroSistema.registrar_error(str(error))

    def limpiar_campos_cliente(self):

        for campo in (
            self.nombre_cliente,
            self.documento_cliente,
            self.correo_cliente,
            self.telefono_cliente
        ):
            campo.delete(0, tk.END)

    def actualizar_lista_clientes(self):

        self.lista_clientes_reserva["values"] = [
            f"{c.identificador} - {c.nombre}"
            for c in self.clientes
        ]

    # ======================================================
    # SERVICIOS
    # ======================================================

    def crear_pagina_servicios(self):

        self.titulo_seccion(
            self.pagina_servicios,
            "Gestion de servicios",
            "Administra salas, alquiler de equipos y asesorias."
        )

        formulario = tk.Frame(
            self.pagina_servicios,
            bg="white"
        )

        formulario.pack(fill="x", padx=20)

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        self.nombre_servicio = self.crear_campo(
            formulario, "Nombre del servicio", 0, 0
        )

        self.precio_servicio = self.crear_campo(
            formulario, "Precio base", 0, 1
        )

        tk.Label(
            formulario,
            text="Tipo de servicio",
            bg="white",
            fg="#34495E",
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=8,
            pady=5
        )

        self.tipo_servicio = ttk.Combobox(
            formulario,
            values=["Sala", "Equipo", "Asesoria"],
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.tipo_servicio.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=8,
            pady=5,
            ipady=5
        )

        self.tipo_servicio.set("Sala")

        self.dato_servicio = self.crear_campo(
            formulario,
            "Capacidad / Tipo de equipo / Especialidad",
            2,
            1
        )

        botones_servicios = tk.Frame(
            self.pagina_servicios,
            bg="white"
        )

        botones_servicios.pack(
            fill="x",
            padx=25,
            pady=12
        )

        self.crear_boton(
            botones_servicios,
            "+ Crear servicio",
            self.registrar_servicio,
            "#188977"
        ).pack(side="right", padx=5)

        self.crear_boton(
            botones_servicios,
            "Eliminar servicio seleccionado",
            self.eliminar_servicio,
            "#B94A48"
        ).pack(side="right", padx=5)

        tk.Label(
            self.pagina_servicios,
            text="SERVICIOS DISPONIBLES",
            bg="white",
            fg="#17365D",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=28, pady=(8, 5))

        self.tabla_servicios = self.crear_tabla(
            self.pagina_servicios,
            ("id", "nombre", "tipo", "precio", "detalle"),
            {
                "id": "ID",
                "nombre": "Servicio",
                "tipo": "Tipo",
                "precio": "Precio base",
                "detalle": "Descripcion"
            },
            {
                "id": 65,
                "nombre": 180,
                "tipo": 100,
                "precio": 120,
                "detalle": 300
            },
            altura=9
        )

    def registrar_servicio(self):

        try:

            nombre = self.nombre_servicio.get().strip()
            precio = self.precio_servicio.get().strip()
            tipo = self.tipo_servicio.get()
            detalle = self.dato_servicio.get().strip()

            if not nombre or not precio or not detalle:
                raise ErrorValidacion(
                    "Complete todos los campos del servicio."
                )

            precio = float(precio.replace(",", "."))

            identificador = f"S{self.contador_servicio:03d}"

            if tipo == "Sala":

                servicio = ServicioSala(
                    identificador,
                    nombre,
                    precio,
                    int(detalle)
                )

            elif tipo == "Equipo":

                servicio = ServicioEquipo(
                    identificador,
                    nombre,
                    precio,
                    detalle
                )

            elif tipo == "Asesoria":

                servicio = ServicioAsesoria(
                    identificador,
                    nombre,
                    precio,
                    detalle
                )

            else:
                raise ErrorValidacion(
                    "Seleccione un tipo de servicio valido."
                )

            self.servicios.append(servicio)
            self.contador_servicio += 1

            self.agregar_servicio_tabla(
                servicio,
                tipo,
                detalle
            )

            self.actualizar_resumen()
            self.actualizar_lista_servicios()

            self.nombre_servicio.delete(0, tk.END)
            self.precio_servicio.delete(0, tk.END)
            self.dato_servicio.delete(0, tk.END)

            messagebox.showinfo(
                "Servicio creado",
                "El servicio fue registrado correctamente."
            )

        except (ValueError, ErrorValidacion, ErrorServicio) as error:

            messagebox.showerror(
                "Error de servicio",
                str(error)
            )

            RegistroSistema.registrar_error(str(error))

    def eliminar_servicio(self):

        seleccion = self.tabla_servicios.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccion requerida",
                "Seleccione el servicio que desea eliminar."
            )
            return

        valores = self.tabla_servicios.item(
            seleccion[0],
            "values"
        )

        identificador = valores[0]

        servicio = next(
            (
                s for s in self.servicios
                if s.identificador == identificador
            ),
            None
        )

        if servicio is None:
            return

        reservas_relacionadas = [
            reserva
            for reserva in self.gestor.listar_reservas()
            if reserva.servicio.identificador == identificador
        ]

        if reservas_relacionadas:
            messagebox.showwarning(
                "No se puede eliminar",
                "Este servicio esta relacionado con una o mas "
                "reservas. No se puede eliminar para conservar "
                "el historial."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            f"¿Esta seguro de eliminar el servicio "
            f"{servicio.nombre}?"
        )

        if not confirmar:
            return

        self.servicios.remove(servicio)
        self.tabla_servicios.delete(seleccion[0])

        self.actualizar_lista_servicios()
        self.actualizar_resumen()

        RegistroSistema.registrar_evento(
            f"Servicio {identificador} eliminado."
        )

        messagebox.showinfo(
            "Servicio eliminado",
            "El servicio fue eliminado correctamente."
        )

    def agregar_servicio_tabla(self, servicio, tipo=None, detalle=None):

        if tipo is None:

            if isinstance(servicio, ServicioSala):
                tipo = "Sala"

            elif isinstance(servicio, ServicioEquipo):
                tipo = "Equipo"

            else:
                tipo = "Asesoria"

            detalle = servicio.describir_servicio()

        self.tabla_servicios.insert(
            "",
            "end",
            values=(
                servicio.identificador,
                servicio.nombre,
                tipo,
                f"${servicio.precio_base:,.2f}",
                detalle
            )
        )

    def cargar_servicios_iniciales(self):

        iniciales = [

            ServicioSala(
                "S001",
                "Sala de reuniones",
                50000,
                20
            ),

            ServicioEquipo(
                "S002",
                "Computador portatil",
                30000,
                "Equipo de computo"
            ),

            ServicioAsesoria(
                "S003",
                "Asesoria en programacion",
                80000,
                "Desarrollo de software"
            )
        ]

        self.servicios.extend(iniciales)
        self.contador_servicio = 4

        for servicio in iniciales:
            self.agregar_servicio_tabla(servicio)

        self.actualizar_lista_servicios()
        self.actualizar_resumen()

    def actualizar_lista_servicios(self):

        if hasattr(self, "lista_servicios_reserva"):

            self.lista_servicios_reserva["values"] = [
                f"{s.identificador} - {s.nombre}"
                for s in self.servicios
            ]

            seleccionado = self.lista_servicios_reserva.get()

            if seleccionado:

                existe = any(
                    seleccionado == f"{s.identificador} - {s.nombre}"
                    for s in self.servicios
                )

                if not existe:
                    self.lista_servicios_reserva.set("")

    # ======================================================
    # RESERVAS
    # ======================================================

    def crear_pagina_reservas(self):

        self.titulo_seccion(
            self.pagina_reservas,
            "Gestion de reservas",
            "Crea, confirma, procesa, finaliza y cancela reservas."
        )

        formulario = tk.Frame(
            self.pagina_reservas,
            bg="white"
        )

        formulario.pack(fill="x", padx=20)

        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        tk.Label(
            formulario,
            text="Seleccionar cliente",
            bg="white",
            fg="#34495E",
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=8,
            pady=5
        )

        self.lista_clientes_reserva = ttk.Combobox(
            formulario,
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.lista_clientes_reserva.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=8,
            pady=5,
            ipady=5
        )

        tk.Label(
            formulario,
            text="Seleccionar servicio",
            bg="white",
            fg="#34495E",
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=8,
            pady=5
        )

        self.lista_servicios_reserva = ttk.Combobox(
            formulario,
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.lista_servicios_reserva.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=8,
            pady=5,
            ipady=5
        )

        self.lista_servicios_reserva.bind(
            "<<ComboboxSelected>>",
            self.actualizar_duracion
        )

        tk.Label(
            formulario,
            text="Duracion (horas o unidades)",
            bg="white",
            fg="#34495E",
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=8,
            pady=5
        )

        self.duracion_reserva = tk.Entry(
            formulario,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.duracion_reserva.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=8,
            pady=5,
            ipady=7
        )

        self.crear_boton(
            self.pagina_reservas,
            "+ Crear reserva",
            self.crear_reserva,
            "#7952A0"
        ).pack(anchor="e", padx=30, pady=8)

        tk.Label(
            self.pagina_reservas,
            text="ACCIONES SOBRE LA RESERVA SELECCIONADA",
            bg="white",
            fg="#17365D",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=28, pady=(8, 5))

        botones = tk.Frame(
            self.pagina_reservas,
            bg="white"
        )

        botones.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.crear_boton(
            botones,
            "Confirmar",
            self.confirmar_reserva,
            "#2471A3"
        ).pack(side="left", padx=3)

        self.crear_boton(
            botones,
            "Procesar",
            self.procesar_reserva,
            "#188977"
        ).pack(side="left", padx=3)

        self.crear_boton(
            botones,
            "Finalizar anticipadamente",
            self.finalizar_reserva_anticipadamente,
            "#7952A0"
        ).pack(side="left", padx=3)

        self.crear_boton(
            botones,
            "Cancelar",
            self.cancelar_reserva,
            "#B94A48"
        ).pack(side="left", padx=3)

        tk.Label(
            self.pagina_reservas,
            text="Seleccione una reserva de la tabla para utilizar los botones.",
            bg="white",
            fg="#718096",
            font=("Segoe UI", 8)
        ).pack(anchor="w", padx=28, pady=4)

        tk.Label(
            self.pagina_reservas,
            text="RESERVAS REGISTRADAS",
            bg="white",
            fg="#17365D",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=28, pady=(5, 5))

        self.tabla_reservas = self.crear_tabla(
            self.pagina_reservas,
            (
                "id",
                "cliente",
                "servicio",
                "duracion",
                "estado",
                "costo"
            ),
            {
                "id": "ID",
                "cliente": "Cliente",
                "servicio": "Servicio",
                "duracion": "Duracion",
                "estado": "Estado",
                "costo": "Costo"
            },
            {
                "id": 70,
                "cliente": 150,
                "servicio": 180,
                "duracion": 120,
                "estado": 160,
                "costo": 120
            },
            altura=5
        )

    # ======================================================
    # ACTUALIZAR LISTAS Y DURACION
    # ======================================================

    def actualizar_duracion(self, evento=None):

        seleccionado = self.lista_servicios_reserva.get()

        if not seleccionado:
            return

        servicio = self.buscar_servicio_seleccionado(
            seleccionado
        )

        if isinstance(servicio, ServicioEquipo):

            self.duracion_reserva.delete(0, tk.END)
            self.duracion_reserva.insert(0, "1")

    def buscar_servicio_seleccionado(self, seleccionado):

        identificador = seleccionado.split(" - ")[0]

        for servicio in self.servicios:

            if servicio.identificador == identificador:
                return servicio

        return None

    # ======================================================
    # CREAR RESERVA
    # ======================================================

    def crear_reserva(self):

        try:

            cliente_seleccionado = self.lista_clientes_reserva.get()
            servicio_seleccionado = self.lista_servicios_reserva.get()
            duracion = self.duracion_reserva.get().strip()

            if (
                not cliente_seleccionado
                or not servicio_seleccionado
                or not duracion
            ):
                raise ErrorValidacion(
                    "Seleccione un cliente, un servicio e indique "
                    "la duracion."
                )

            id_cliente = cliente_seleccionado.split(" - ")[0]

            cliente = next(
                c for c in self.clientes
                if c.identificador == id_cliente
            )

            servicio = self.buscar_servicio_seleccionado(
                servicio_seleccionado
            )

            if servicio is None:
                raise ErrorServicio(
                    "El servicio seleccionado ya no existe."
                )

            reserva = self.gestor.crear_reserva(
                f"R{self.contador_reserva:03d}",
                cliente,
                servicio,
                int(duracion)
            )

            self.contador_reserva += 1

            self.actualizar_tabla_reservas()
            self.duracion_reserva.delete(0, tk.END)

            messagebox.showinfo(
                "Reserva creada",
                f"La reserva {reserva.identificador} "
                "fue creada correctamente."
            )

        except (
            ValueError,
            StopIteration,
            ErrorValidacion,
            ErrorServicio,
            ErrorReserva
        ) as error:

            messagebox.showerror(
                "Error de reserva",
                str(error)
            )

            RegistroSistema.registrar_error(str(error))

    # ======================================================
    # OBTENER RESERVA SELECCIONADA
    # ======================================================

    def obtener_reserva_seleccionada(self):

        seleccion = self.tabla_reservas.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccion requerida",
                "Seleccione una reserva de la tabla."
            )

            return None

        identificador = self.tabla_reservas.item(
            seleccion[0],
            "values"
        )[0]

        return self.gestor.buscar_reserva(identificador)

    # ======================================================
    # CONFIRMAR RESERVA
    # ======================================================

    def confirmar_reserva(self):

        try:

            reserva = self.obtener_reserva_seleccionada()

            if reserva is None:
                return

            mensaje = reserva.confirmar()

            self.actualizar_tabla_reservas()

            messagebox.showinfo(
                "Reserva",
                mensaje
            )

        except ErrorReserva as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            RegistroSistema.registrar_error(str(error))

    # ======================================================
    # PROCESAR RESERVA
    # ======================================================

    def procesar_reserva(self):

        try:

            reserva = self.obtener_reserva_seleccionada()

            if reserva is None:
                return

            total = reserva.procesar()

            self.actualizar_tabla_reservas()

            messagebox.showinfo(
                "Reserva procesada",
                f"El total de la reserva es: ${total:,.2f}"
            )

        except ErrorReserva as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            RegistroSistema.registrar_error(str(error))

    # ======================================================
    # FINALIZAR ANTICIPADAMENTE
    # ======================================================

    def finalizar_reserva_anticipadamente(self):

        try:

            reserva = self.obtener_reserva_seleccionada()

            if reserva is None:
                return

            if reserva.estado != "Confirmada":

                messagebox.showwarning(
                    "Reserva no disponible",
                    "La reserva debe estar confirmada para "
                    "finalizarla anticipadamente."
                )

                return

            duracion_real = simpledialog.askinteger(
                "Finalizar anticipadamente",
                f"Duracion reservada: {reserva.duracion}\n\n"
                f"Ingrese las horas o unidades realmente "
                f"utilizadas (de 1 a {reserva.duracion - 1}):",
                parent=self.ventana,
                minvalue=1,
                maxvalue=reserva.duracion - 1
            )

            if duracion_real is None:
                return

            total = reserva.finalizar_anticipadamente(
                duracion_real
            )

            self.actualizar_tabla_reservas()

            messagebox.showinfo(
                "Reserva finalizada",
                f"La reserva fue finalizada anticipadamente.\n\n"
                f"Duracion reservada: {reserva.duracion}\n"
                f"Duracion real: {duracion_real}\n"
                f"Costo final: ${total:,.2f}"
            )

        except (ErrorValidacion, ErrorReserva) as error:

            messagebox.showerror(
                "Error al finalizar",
                str(error)
            )

            RegistroSistema.registrar_error(str(error))

    # ======================================================
    # CANCELAR RESERVA
    # ======================================================

    def cancelar_reserva(self):

        try:

            reserva = self.obtener_reserva_seleccionada()

            if reserva is None:
                return

            confirmar = messagebox.askyesno(
                "Confirmar cancelacion",
                f"¿Desea cancelar la reserva "
                f"{reserva.identificador}?"
            )

            if not confirmar:
                return

            mensaje = reserva.cancelar()

            self.actualizar_tabla_reservas()

            messagebox.showinfo(
                "Reserva",
                mensaje
            )

        except ErrorReserva as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

            RegistroSistema.registrar_error(str(error))

    # ======================================================
    # ACTUALIZAR TABLA DE RESERVAS
    # ======================================================

    def actualizar_tabla_reservas(self):

        for elemento in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(elemento)

        for reserva in self.gestor.listar_reservas():

            duracion_real = getattr(
                reserva,
                "duracion_real",
                None
            )

            if duracion_real is not None:

                duracion_mostrada = (
                    f"{reserva.duracion} "
                    f"(real: {duracion_real})"
                )

            else:

                duracion_mostrada = reserva.duracion

            self.tabla_reservas.insert(
                "",
                "end",
                values=(
                    reserva.identificador,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    duracion_mostrada,
                    reserva.estado,
                    f"${reserva.costo:,.2f}"
                )
            )

        self.actualizar_resumen()


# ==========================================================
# EJECUCION DE LA APLICACION
# ==========================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    aplicacion = AplicacionSoftwareFJ(ventana)

    ventana.mainloop()
