from PyQt5.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QListWidgetItem, QListWidget,QHBoxLayout)
from PyQt5.QtWidgets import QWidget, QVBoxLayout,QScrollArea, QPushButton,QComboBox,QGroupBox
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
import Administrador
import Cocinero
import Plato
import Pedido
import Ingredientes
import sys

# Función para limpiar la pantalla (elimina todos los widgets)
def limpiar_pantalla(contenedor):
    while contenedor.count():
        child = contenedor.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            limpiar_pantalla(child.layout())

# Estilo predeterminado botones con fondo png
def diseño_boton(texto, tamaño=14):
    boton = QPushButton(texto)
    boton.setFont(QFont("Helvetica", tamaño, QFont.Bold))
    boton.setStyleSheet(f"background-image: url(Iconos//Fondo Boton.png); "
                        "color: #ffffff; border: none;")
    boton.setFixedSize(180, 50)  # Ajusta el tamaño del botón
    return boton


# Pantalla Inicial
def pantalla_inicial(frame):
    
    
    # Limpia la pantalla
    limpiar_pantalla(frame)

    #logo de la app
    logo_label = QLabel()
    pixmap = QPixmap("Iconos\\Digital Order Logo.png")
    pixmap_redimensionado = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    logo_label.setPixmap(pixmap_redimensionado)
    logo_label.setAlignment(Qt.AlignCenter)
    frame.addWidget(logo_label)

    # Botón Seleccionar Mesa
    boton_mesa = diseño_boton("Seleccionar \n Mesa")
    boton_mesa.clicked.connect(lambda: seleccionar_mesa(frame))
    frame.addWidget(boton_mesa, alignment=Qt.AlignCenter)

    # Botón Iniciar sesión Administrador
    boton_admin = diseño_boton("Iniciar Sesión \n Admin")
    boton_admin.clicked.connect(lambda: iniciar_sesion(frame))
    frame.addWidget(boton_admin, alignment=Qt.AlignCenter)

    # Botón Iniciar sesión Cocinero
    boton_cocinero = diseño_boton("Iniciar Sesión \n Cocinero")
    boton_cocinero.clicked.connect(lambda: iniciar_sesion_cocinero(frame))
    frame.addWidget(boton_cocinero,alignment=Qt.AlignCenter)

    # Carga la imagen de Chef y la redimensiona
    imagen_label = QLabel()
    pixmap = QPixmap("Iconos\\Chef.png")
    pixmap_redimensionado = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    imagen_label.setPixmap(pixmap_redimensionado)
    imagen_label.setAlignment(Qt.AlignCenter)
    frame.addWidget(imagen_label)

# Pantalla de Selección de Mesas
def seleccionar_mesa(frame):
    # Limpia la pantalla
    limpiar_pantalla(frame)

    # Etiqueta de selección de mesa
    etiqueta_seleccion = QLabel("Selecciona una mesa:")
    etiqueta_seleccion.setFont(QFont("Helvetica", 18, QFont.Bold))
    etiqueta_seleccion.setStyleSheet("color: #000000; background-color: #d9b5a9;")
    etiqueta_seleccion.setAlignment(Qt.AlignCenter)
    frame.addWidget(etiqueta_seleccion)

    # Crea un layout en forma de cuadrícula para las mesas
    grid_layout = QGridLayout()
    frame.addLayout(grid_layout)

    # Crea 20 mesas
    for i in range(1, 21):
         boton_mesa = QPushButton(f"Mesa {i}")
         boton_mesa.setFont(QFont("Helvetica", 14, QFont.Bold))  
         boton_mesa.setStyleSheet("background-color: #ffffff;") 
         boton_mesa.setFixedSize(100, 40) 
         boton_mesa.clicked.connect(lambda checked, mesa=i: mostrar_menu(frame, mesa))
         boton_mesa.setStyleSheet("""
            background-color: #f4f4f4;
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 10px;                    
            """)
        
        # Agregar el botón en la cuadrícula
         fila = (i - 1) // 5  # Calcula la fila
         columna = (i - 1) % 5  # Calcula la columna
         grid_layout.addWidget(boton_mesa, fila, columna)

    # Botón para volver atrás
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: pantalla_inicial(frame))
    frame.addWidget(boton_volver,alignment=Qt.AlignCenter)

# Pantalla de Menú de Platos 
def mostrar_menu(frame, mesa):
    limpiar_pantalla(frame)

    # Etiqueta del menú para la mesa seleccionada
    etiqueta_menu = QLabel(f"Menú para la Mesa {mesa}")
    etiqueta_menu.setFont(QFont("Helvetica", 18, QFont.Bold))
    etiqueta_menu.setStyleSheet("color: #000000; background-color: #d9b5a9;")
    etiqueta_menu.setAlignment(Qt.AlignCenter)
    frame.addWidget(etiqueta_menu)

    # Crear una lista para mostrar los platos
    lista_platos = QListWidget()
    frame.addWidget(lista_platos)

    #Muestra la base de datos de Platos
    platos = Plato.mostrar_menu()

    # Función para crear un widget personalizado para cada plato
    def item_personalizado(nombre, descripcion, precio):
        widget = QWidget()
        layout = QVBoxLayout()

        # Ajustar el espaciado entre los elementos
        layout.setSpacing(5)

        # Etiqueta del nombre del plato
        label_nombre = QLabel(nombre)
        label_nombre.setFont(QFont("Helvetica", 14, QFont.Bold))
        label_nombre.setStyleSheet("color: #0a0a0a;")

        # Etiqueta de la descripción del plato
        label_descripcion = QLabel(descripcion)
        label_descripcion.setFont(QFont("Arial", 10))
        label_descripcion.setStyleSheet("color: #555555;")

        # Etiqueta del precio del plato
        label_precio = QLabel(f"${precio:.2f}")
        label_precio.setFont(QFont("Helvetica", 11))
        label_precio.setStyleSheet("color: #008f39;")

        # Agregar las etiquetas al layout
        layout.addWidget(label_nombre)
        layout.addWidget(label_descripcion)
        layout.addWidget(label_precio)

        # Asignar el layout al widget
        widget.setLayout(layout)

        return widget

    # Cargar los platos a la lista
    for nombre, descripcion, precio in platos:
        item = QListWidgetItem(lista_platos)  
        widget_personalizado = item_personalizado(nombre, descripcion, precio)
        lista_platos.setItemWidget(item, widget_personalizado)
        item.setSizeHint(widget_personalizado.sizeHint())

    # Aplica el estilo hover a la lista
    lista_platos.setStyleSheet("""
        QListWidget::item {
            padding: 1px; /* Espaciado */
        }
        QListWidget::item:hover {
            background-color: #e6ccbb;  /* Fondo al pasar el mouse */
        }
        QListWidget::item:selected {
            background-color: #b8daba;  /* Fondo cuando está seleccionado */
        }
    """)

    # Etiqueta con el precio total del pedido
    total_pedido = 0  
    etiqueta_total = QLabel(f"Total de su Pedido: ${total_pedido:.2f}")
    etiqueta_total.setFont(QFont("Helvetica", 14))
    etiqueta_total.setStyleSheet("color: #000000; background-color: #d9b5a9;")
    frame.addWidget(etiqueta_total)

    # Crea el carrito para el pedido
    pedido_id = Pedido.crear_carrito()

    # Función para actualizar el total al hacer clic en un plato
    def plato_seleccionado(item):
        nonlocal total_pedido  
        row = lista_platos.row(item)  # Obtiene el índice de la fila seleccionada
        precio = platos[row][2]  # Obtiene el precio del plato seleccionado
        plato_id = platos[row][0]
        total_pedido += precio  # Suma el precio al total
        etiqueta_total.setText(f"Total de su Pedido: ${total_pedido:.2f}")
        
        # Agrega el plato al carrito
        cantidad = 1 
        Pedido.agregar_al_carrito(pedido_id, plato_id, cantidad)

    # Conecta la señal de clic de la lista
    lista_platos.itemClicked.connect(plato_seleccionado)

    # Botón para confirmar el pedido
    boton_confirmar = diseño_boton("Confirmar Pedido")
    boton_confirmar.clicked.connect(lambda: [Pedido.confirmar_pedido(pedido_id, mesa), pedido_confirmado(frame)])
    frame.addWidget(boton_confirmar, alignment=Qt.AlignCenter)

    #Boton para ver el carrito
    boton_carrito =diseño_boton("Carrito")
    boton_carrito.clicked.connect(lambda: mostrar_carrito(frame, mesa, pedido_id))
    frame.addWidget(boton_carrito, alignment=Qt.AlignCenter)

    # Botón para volver atrás
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: seleccionar_mesa(frame))
    frame.addWidget(boton_volver, alignment=Qt.AlignCenter)

#Pantalla Pedido Confirmado
def pedido_confirmado(frame):
    #limpia la pantalla
    limpiar_pantalla(frame)

    # Etiqueta pedido confirmado
    etiqueta_pedido_confirmado = QLabel("Pedido Confirmado! ")
    etiqueta_pedido_confirmado.setFont(QFont("Helvetica", 18, QFont.Bold))
    etiqueta_pedido_confirmado.setAlignment(Qt.AlignCenter)
    frame.addWidget(etiqueta_pedido_confirmado)

    # Botón para volver atrás
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: pantalla_inicial(frame))
    frame.addWidget(boton_volver,alignment=Qt.AlignCenter)

# Pantalla Mostrar Carrito
def mostrar_carrito(frame, mesa, pedido_id):
    # Limpia la pantalla
    limpiar_pantalla(frame)

    # Etiqueta para el carrito
    etiqueta_carrito = QLabel("Carrito: ")
    etiqueta_carrito.setFont(QFont("Helvetica", 18, QFont.Bold))
    etiqueta_carrito.setAlignment(Qt.AlignCenter)
    frame.addWidget(etiqueta_carrito)

    # Crea una lista para mostrar los platos del carrito
    lista_carrito = QListWidget()
    frame.addWidget(lista_carrito)

    # Carga los platos en el carrito
    pedido = Pedido.mostrar_carrito(pedido_id)

    total_carrito = 0  # Variable para acumular el total del carrito
    
    for plato_id, nombre, precio, cantidad in pedido:
         item_text = f"{nombre} - Cantidad: {cantidad} - Precio: ${precio:.2f}"
         item = QListWidgetItem(item_text)
         item.setFont(QFont("Helvetica", 12))
         lista_carrito.addItem(item)  # Agrega el item a la lista

         total_carrito += precio * cantidad  # Suma el total del carrito

    # Etiqueta con el total del pedido
    etiqueta_total = QLabel(f"Total de su Pedido: ${total_carrito:.2f}")
    etiqueta_total.setFont(QFont("Helvetica", 14))
    etiqueta_total.setStyleSheet("color: #000000; background-color: #d9b5a9;")
    frame.addWidget(etiqueta_total)

    # Crea un layout horizontal para los botones
    boton_layout = QHBoxLayout()

    # Botón para borrar el plato
    boton_borrar_pedido = diseño_boton("Eliminar \n Plato")
    boton_borrar_pedido.clicked.connect(lambda: actualizar_carrito(frame, mesa, pedido_id, lista_carrito, "eliminar"))
    boton_layout.addWidget(boton_borrar_pedido)

    # Botón para reducir cantidad de un plato
    boton_borrar_cantidad = diseño_boton("Reducir \n Cantidad")
    boton_borrar_cantidad.clicked.connect(lambda: actualizar_carrito(frame, mesa, pedido_id, lista_carrito, "reducir"))
    boton_layout.addWidget(boton_borrar_cantidad)

    # Botón para aumentar cantidad de un plato
    boton_aumentar_cantidad = diseño_boton("Aumentar \n Cantidad")
    boton_aumentar_cantidad.clicked.connect(lambda: actualizar_carrito(frame, mesa, pedido_id, lista_carrito, "aumentar"))
    boton_layout.addWidget(boton_aumentar_cantidad)

    # Añade los botones al frame
    frame.addLayout(boton_layout)

    # Botón para confirmar el pedido
    boton_confirmar = diseño_boton("Confirmar Pedido")
    boton_confirmar.clicked.connect(lambda: [Pedido.confirmar_pedido(pedido_id, mesa), pedido_confirmado(frame)])
    frame.addWidget(boton_confirmar, alignment=Qt.AlignCenter)

    # Botón para volver al menú
    boton_volver_menu = diseño_boton("Volver")
    boton_volver_menu.clicked.connect(lambda: mostrar_menu(frame, mesa))
    frame.addWidget(boton_volver_menu, alignment=Qt.AlignCenter)

#Funcion que actualiza el carrito
def actualizar_carrito(frame, mesa, pedido_id, lista_carrito, accion):
    # Obtener el plato seleccionado
    selected_item = lista_carrito.currentItem()
    if selected_item:
        plato_index = lista_carrito.row(selected_item)
        plato_id, nombre, precio, cantidad = Pedido.mostrar_carrito(pedido_id)[plato_index]

        if accion == "eliminar":
            Pedido.eliminar_del_carrito(pedido_id, plato_id)
        elif accion == "reducir":
            Pedido.reducir_cantidad(cantidad, pedido_id, plato_id)
        elif accion == "aumentar":
            Pedido.aumentar_cantidad(cantidad, pedido_id, plato_id)

        # Actualizar la vista del carrito
        mostrar_carrito(frame, mesa, pedido_id)

def mostrar_pedidos(frame):
    # Consulta para obtener los pedidos
    pedidos = Pedido.obtener_pedidos()  # Usamos el método que ya tienes para obtener los pedidos
    
    # Obtener lista de cocineros
    lista_cocineros = Cocinero.obtener_cocineros()  # Esta debe devolver los nombres de los cocineros

    # Limpiar la pantalla
    limpiar_pantalla(frame)

    # Crear un QScrollArea para los pedidos
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    # Crear el widget que contendrá los pedidos
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)

    # Layout para los pedidos
    for pedido in pedidos:
        pedido_id, numero_mesa, plato, cantidad, estado = pedido

        # Crear una caja para cada pedido
        group_box = QGroupBox(f"Pedido #{pedido_id} - Mesa: {numero_mesa}")
        layout_pedido = QVBoxLayout()

        # Mostrar platos del pedido
        layout_pedido.addWidget(QLabel(f"Plato: {plato}, Cantidad: {cantidad}"))
        layout_pedido.addWidget(QLabel(f"Estado actual: {estado}"))

        # ComboBox para elegir cocinero
        cocinero_combo = QComboBox()
        cocinero_combo.addItems(lista_cocineros)  # Agregar cocineros de la base de datos
        layout_pedido.addWidget(QLabel("Selecciona Cocinero:"))
        layout_pedido.addWidget(cocinero_combo)

        # Botón para confirmar el pedido y asignar cocinero
        confirmar_btn = QPushButton("Confirmar Pedido")
        # Usar un valor por defecto en la función lambda para que capture el pedido_id actual
        confirmar_btn.clicked.connect(lambda _, pid=pedido_id, combo=cocinero_combo: confirmar_pedido(pid, combo))
        layout_pedido.addWidget(confirmar_btn)

        # Añadir el layout del pedido al group box
        group_box.setLayout(layout_pedido)
        scroll_layout.addWidget(group_box)  # Añadir el group_box al layout scroll

    # Establecer el widget de contenido desplazable en el área de scroll
    scroll_content.setLayout(scroll_layout)
    scroll_area.setWidget(scroll_content)

    # Añadir el área de scroll al frame principal
    frame.addWidget(scroll_area)

def confirmar_pedido(pedido_id, cocinero_combo):
    cocinero_seleccionado = cocinero_combo.currentText()
    print(f"Pedido {pedido_id} asignado a {cocinero_seleccionado}")






def iniciar_sesion_cocinero(frame):
    # Limpia la pantalla
    limpiar_pantalla(frame)

    # Etiqueta de Inicio de Sesion para Cocinero
    sesion = QLabel("Inicio de Sesión - Cocinero")
    sesion.setFont(QFont("Helvetica", 18, QFont.Bold))
    sesion.setAlignment(Qt.AlignCenter)
    frame.addWidget(sesion)

    # Campo de usuario
    usuario = QLabel("Usuario:")
    usuario.setFont(QFont("Helvetica", 14))
    usuario.setAlignment(Qt.AlignCenter)
    frame.addWidget(usuario)
    entry_usuario = QLineEdit()
    entry_usuario.setFixedSize(200, 30)  # Establece un ancho de 200 y un alto de 30
    entry_usuario.setStyleSheet("background-color: white;")
    frame.addWidget(entry_usuario, alignment=Qt.AlignCenter)

    # Campo de contraseña
    contraseña = QLabel("Contraseña:")
    contraseña.setFont(QFont("Helvetica", 14))
    contraseña.setAlignment(Qt.AlignCenter)
    frame.addWidget(contraseña)
    entry_contraseña = QLineEdit()
    entry_contraseña.setFixedSize(200, 30)  # Establece un ancho de 200 y un alto de 30
    entry_contraseña.setStyleSheet("background-color: white;")
    entry_contraseña.setEchoMode(QLineEdit.Password)
    frame.addWidget(entry_contraseña, alignment=Qt.AlignCenter)

    # Botón para mostrar u ocultar la contraseña
    boton_mostrar = diseño_boton("Mostrar Contraseña", tamaño=12)
    boton_mostrar.clicked.connect(lambda: mostrar_contraseña(entry_contraseña))
    frame.addWidget(boton_mostrar, alignment=Qt.AlignCenter)

    # Botón para iniciar sesión como Cocinero
    boton_login = diseño_boton("Iniciar Sesión")
    boton_login.clicked.connect(lambda: confirmar_login_cocinero(entry_usuario, entry_contraseña,frame))
    frame.addWidget(boton_login, alignment=Qt.AlignCenter)

    # Botón para volver a la pantalla inicial
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: pantalla_inicial(frame))
    frame.addWidget(boton_volver, alignment=Qt.AlignCenter)

# Función para confirmar el inicio de sesión
def confirmar_login_cocinero(entry_usuario, entry_contraseña,frame):
    usuario = entry_usuario.text()
    contraseña = entry_contraseña.text()

    # Si el usuario y/o contraseña son vacíos o incorrectos, se imprimen en la pantalla
    if not usuario or not contraseña:
        mensaje_error = QLabel("Usuario y/o contraseña vacíos")
        mensaje_error.setStyleSheet("color: red;")
        frame.layout().addWidget(mensaje_error)
    else:
        # Valida el administrador
        islogin = Cocinero.validar_Cocinero(usuario, contraseña)
        if islogin:
            mostrar_pedidos(frame) 
        else:
            mensaje_error = QLabel("Usuario y/o contraseña incorrectos")
            mensaje_error.setStyleSheet("color: red;")
            frame.layout().addWidget(mensaje_error)


#Pantalla inicio de sesion Administrador
def iniciar_sesion(frame):
    # Limpia la pantalla
    limpiar_pantalla(frame)

    # Etiqueta de Inicio de Sesion
    sesion=QLabel("Inicio de Sesión")
    sesion.setFont(QFont("Helvetica", 18, QFont.Bold))
    sesion.setAlignment(Qt.AlignCenter)
    frame.addWidget(sesion)

    # Campo de usuario
    usuario = QLabel("Usuario:")
    usuario.setFont(QFont("Helvetica", 14))
    usuario.setAlignment(Qt.AlignCenter)
    frame.addWidget(usuario)
    entry_usuario = QLineEdit()
    entry_usuario.setFixedSize(200, 30)  # Establece un ancho de 200 y un alto de 30
    entry_usuario.setStyleSheet("background-color: white;")
    frame.addWidget(entry_usuario, alignment=Qt.AlignCenter)

    # Campo de contraseña
    contraseña = QLabel("Contraseña:")
    contraseña.setFont(QFont("Helvetica", 14))
    contraseña.setAlignment(Qt.AlignCenter)
    frame.addWidget(contraseña)
    entry_contraseña = QLineEdit()
    entry_contraseña.setFixedSize(200, 30)  # Establece un ancho de 200 y un alto de 30
    entry_contraseña.setStyleSheet("background-color: white;")
    entry_contraseña.setEchoMode(QLineEdit.Password)
    frame.addWidget(entry_contraseña,alignment=Qt.AlignCenter)

    # Botón para mostrar u ocultar la contraseña
    boton_mostrar = diseño_boton("Mostrar Contraseña",tamaño=12)
    boton_mostrar.clicked.connect(lambda: mostrar_contraseña(entry_contraseña))
    frame.addWidget(boton_mostrar,alignment=Qt.AlignCenter)

    # Botón para iniciar sesión
    boton_login = diseño_boton("Iniciar Sesión")
    boton_login.clicked.connect(lambda: confirmar_login(entry_usuario, entry_contraseña, frame))
    frame.addWidget(boton_login,alignment=Qt.AlignCenter)

    # Botón para volver a la pantalla inicial
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: pantalla_inicial(frame))
    frame.addWidget(boton_volver, alignment=Qt.AlignCenter)

# Función para mostrar la contraseña
def mostrar_contraseña(entry_contraseña):
    if entry_contraseña.echoMode() == QLineEdit.Password:
        entry_contraseña.setEchoMode(QLineEdit.Normal)
    else:
        entry_contraseña.setEchoMode(QLineEdit.Password)

# Función para confirmar el inicio de sesión
def confirmar_login(entry_usuario, entry_contraseña, frame):
    usuario = entry_usuario.text()
    contraseña = entry_contraseña.text()

    # Si el usuario y/o contraseña son vacíos o incorrectos, se imprimen en la pantalla
    if not usuario or not contraseña:
        mensaje_error = QLabel("Usuario y/o contraseña vacíos")
        mensaje_error.setStyleSheet("color: red;")
        frame.layout().addWidget(mensaje_error)
    else:
        # Valida el administrador
        islogin = Administrador.validar_administrador(usuario, contraseña)
        if islogin:
            menu_admin(frame) 
        else:
            mensaje_error = QLabel("Usuario y/o contraseña incorrectos")
            mensaje_error.setStyleSheet("color: red;")
            frame.layout().addWidget(mensaje_error)

# Pantalla del menú del Administrador
def menu_admin(frame):
    # Limpiar la pantalla
    limpiar_pantalla(frame)

    # Etiqueta del panel de administración
    label_menu = QLabel("Panel de Administración")
    label_menu.setFont(QFont("Helvetica", 18, QFont.Bold))
    label_menu.setAlignment(Qt.AlignCenter)
    frame.addWidget(label_menu)

    # Crear un layout horizontal para los botones de agregar y modificar
    h_layout_admin = QHBoxLayout()
    
    # Botón para agregar administrador
    boton_agregar_admin = diseño_boton("Agregar \n Administrador")
    boton_agregar_admin.clicked.connect(lambda: agregar_admin(frame))
    h_layout_admin.addWidget(boton_agregar_admin)

    # Botón para modificar administrador
    boton_modificar_admin = diseño_boton("Modificar \n Administrador")
    boton_modificar_admin.clicked.connect(lambda: modificar_admin(frame))
    h_layout_admin.addWidget(boton_modificar_admin)

    # Agregar el layout horizontal al frame
    frame.addLayout(h_layout_admin)

    # Crear un layout horizontal para los botones de editar
    h_layout_editar = QHBoxLayout()
    
    # Botón para editar menú
    boton_editar_menu = diseño_boton("Editar Menú")
    boton_editar_menu.clicked.connect(lambda: editar_menu(frame))
    h_layout_editar.addWidget(boton_editar_menu)

    # Botón para editar ingredientes
    boton_editar_ingredientes = diseño_boton("Editar \n Ingredientes")
    boton_editar_ingredientes.clicked.connect(lambda: editar_ingredientes(frame))
    h_layout_editar.addWidget(boton_editar_ingredientes)

    # Agregar el layout horizontal al frame
    frame.addLayout(h_layout_editar)

    # Botón para volver atrás
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: pantalla_inicial(frame))
    frame.addWidget(boton_volver, alignment=Qt.AlignCenter)

# Pantalla para agregar Admin
def agregar_admin(frame):
    #Limpia la Pantalla
    limpiar_pantalla(frame)

    # Etiqueta de agregar Administrador
    label_menu = QLabel("Agregar Administrador")
    label_menu.setFont(QFont("Helvetica", 18, QFont.Bold))
    label_menu.setAlignment(Qt.AlignCenter)
    frame.addWidget(label_menu)

    # Campo de usuario
    usuario = QLabel("Usuario:")
    usuario.setFont(QFont("Helvetica", 14))
    usuario.setAlignment(Qt.AlignCenter)
    frame.addWidget(usuario)
    entry_usuario = QLineEdit()
    entry_usuario.setFixedSize(200, 30)  # Establece un ancho de 200 y un alto de 30
    entry_usuario.setStyleSheet("background-color: white;")
    frame.addWidget(entry_usuario, alignment=Qt.AlignCenter)

    # Campo de contraseña
    contraseña = QLabel("Contraseña (DNI):")
    contraseña.setFont(QFont("Helvetica", 14))
    contraseña.setAlignment(Qt.AlignCenter)
    frame.addWidget(contraseña)
    entry_contraseña = QLineEdit()
    entry_contraseña.setFixedSize(200, 30)  # Establece un ancho de 200 y un alto de 30
    entry_contraseña.setStyleSheet("background-color: white;")
    frame.addWidget(entry_contraseña,alignment=Qt.AlignCenter)

    # Boton agregar administrador
    boton_agregar=diseño_boton("Agregar")
    boton_agregar.clicked.connect(lambda: admin_correcto(frame,entry_usuario.text(),entry_contraseña.text()))
    frame.addWidget(boton_agregar, alignment=Qt.AlignCenter)

    # Botón para volver al menu del administrador
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: menu_admin(frame))
    frame.addWidget(boton_volver, alignment=Qt.AlignCenter)

# Funcion para verificar si el Administrador es Correcto
def admin_correcto(frame, usuario, contraseña):
    # Verificar si los campos están vacíos
    if not usuario or not contraseña:
        mensaje = QLabel("Usuario y/o contraseña vacíos")
        mensaje.setFont(QFont("Helvetica", 14))
        frame.addWidget(mensaje)
        return  

    # Intenta agregar el administrador solo si los campos son válidos
    isCorrect = Administrador.agregar_administrador(usuario, contraseña)
    if isCorrect:
        mensaje = QLabel("Se agregó el usuario correctamente")
        mensaje.setFont(QFont("Helvetica", 14))
        frame.addWidget(mensaje)
    else:
        mensaje = QLabel("Error al agregar el usuario")
        mensaje.setFont(QFont("Helvetica", 14))
        frame.addWidget(mensaje)     

#Pantalla Modificar Admin
def modificar_admin(frame):
    # Limpia la Pantalla
    limpiar_pantalla(frame)

    # Etiqueta de modificar Administrador
    label_menu = QLabel("Modificar Administrador")
    label_menu.setFont(QFont("Helvetica", 18, QFont.Bold))
    label_menu.setAlignment(Qt.AlignCenter)
    frame.addWidget(label_menu)

    # Crea una tabla para mostrar los administradores
    table = QtWidgets.QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["ID", "Usuario", "Contraseña"])
    table.verticalHeader().setVisible(False)
    table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    # Ajustar el ancho de las columnas
    table.setColumnWidth(0, 100)  
    table.setColumnWidth(1, 300)  
    table.setColumnWidth(2, 300)  

    # Fija un tamaño mínimo para la tabla
    table.setMinimumSize(700, 250)

    # Hace que las columnas se ajusten automáticamente
    header = table.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    table.setStyleSheet("background: #FFDBB8;")
    
    # Crea un layout horizontal para la tabla y los inputs
    main_layout = QtWidgets.QHBoxLayout()

    # Añade la tabla al layout principal
    main_layout.addWidget(table, alignment=Qt.AlignCenter)

    # Crea un layout vertical para los labels y los LineEdits
    input_layout = QtWidgets.QVBoxLayout()

    # Inputs ID
    label_id = QLabel("ID")
    label_id.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_id, alignment=Qt.AlignCenter)
    id_ingresado = QtWidgets.QLineEdit()
    id_ingresado.setStyleSheet("background-color: white;")
    input_layout.addWidget(id_ingresado, alignment=Qt.AlignCenter)

    #Inputs Nombre
    label_nombre = QLabel("Nombre")
    label_nombre.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_nombre, alignment=Qt.AlignCenter)
    nombre_nuevo = QtWidgets.QLineEdit()
    nombre_nuevo.setStyleSheet("background-color: white;")
    input_layout.addWidget(nombre_nuevo, alignment=Qt.AlignCenter)

    #Inputs Contraseña
    label_contraseña = QLabel("Contraseña")
    label_contraseña.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_contraseña, alignment=Qt.AlignCenter)
    contraseña_nueva = QtWidgets.QLineEdit()
    contraseña_nueva.setStyleSheet("background-color: white;")
    input_layout.addWidget(contraseña_nueva, alignment=Qt.AlignCenter)

    # Añade el layout de inputs al layout principal
    main_layout.addLayout(input_layout)

    # Añade el layout principal al frame
    frame.addLayout(main_layout)

    # Carga los administradores
    administradores = Administrador.obtener_administradores()
    table.setRowCount(len(administradores))
    for row, admin in enumerate(administradores):
        for col, value in enumerate(admin):
            table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    # Función para manejar la selección de la tabla
    def on_select():
        selected = table.selectedItems()
        if selected:
            id_ingresado.setText(selected[0].text())
            nombre_nuevo.setText(selected[1].text())
            contraseña_nueva.setText(selected[2].text())

    table.itemSelectionChanged.connect(on_select)

    # Crea un layout horizontal para los botones
    button_layout = QtWidgets.QHBoxLayout()

    # Botón para modificar
    btn_modificar = diseño_boton("Modificar")
    btn_modificar.clicked.connect(lambda: [Administrador.actualizar_administrador(id_ingresado.text(), nombre_nuevo.text(), contraseña_nueva.text()),
                                           actualizar_tabla(table, Administrador.obtener_administradores)])
    button_layout.addWidget(btn_modificar)

    # Botón para eliminar
    btn_eliminar = diseño_boton("Eliminar")
    btn_eliminar.clicked.connect(lambda: [Administrador.eliminar_administrador(id_ingresado.text()),
                                          actualizar_tabla(table, Administrador.obtener_administradores)])
    button_layout.addWidget(btn_eliminar)

    # Botón para volver al menu del administrador
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: menu_admin(frame))
    button_layout.addWidget(boton_volver)

    # Añade el layout de botones debajo de la tabla
    frame.addLayout(button_layout)

    # Alinea el layout de botones al centro
    button_layout.setAlignment(Qt.AlignCenter)

#Funcion para actualizar las tablas
def actualizar_tabla(table, obtener_datos_func):
    datos = obtener_datos_func()
    table.setRowCount(len(datos))
    for row, item in enumerate(datos):
        for col, value in enumerate(item):
            table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

#Pantalla Editar Menu
def editar_menu(frame):
    #Limpia pantalla
    limpiar_pantalla(frame)

 # Etiqueta de editar menu
    label_menu = QLabel("Editar Menu")
    label_menu.setFont(QFont("Helvetica", 18, QFont.Bold))
    label_menu.setAlignment(Qt.AlignCenter)
    frame.addWidget(label_menu)

    # Crea una tabla para mostrar el menu
    table = QtWidgets.QTableWidget()
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["ID","Nombre", "Descipcion", "Precio", "Ingredientes"])
    table.verticalHeader().setVisible(False)
    table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    # Ajustar el ancho de las columnas
    table.setColumnWidth(0, 100)  
    table.setColumnWidth(1, 300)   
    table.setColumnWidth(2, 400)   
    table.setColumnWidth(3, 100)  
    table.setColumnWidth(4, 200)  

    # Fija un tamaño mínimo para la tabla
    table.setMinimumSize(700, 250)

    # Hace que las columnas se ajusten automáticamente
    header = table.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    table.setStyleSheet("background: #FFDBB8;")

    # Crea un layout horizontal para la tabla y los inputs
    main_layout = QtWidgets.QHBoxLayout()

    # Añade la tabla al layout principal
    main_layout.addWidget(table, alignment=Qt.AlignCenter)

    # Crea un layout vertical para los labels y QLineEdits
    input_layout = QtWidgets.QVBoxLayout()

    # Inputs ID
    label_id = QLabel("ID")
    label_id.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_id, alignment=Qt.AlignCenter)
    id_ingresado = QtWidgets.QLineEdit()
    id_ingresado.setStyleSheet("background-color: white;")
    input_layout.addWidget(id_ingresado, alignment=Qt.AlignCenter)

    # Inputs Nombre
    label_nombre = QLabel("Nombre")
    label_nombre.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_nombre, alignment=Qt.AlignCenter)
    nombre_nuevo = QtWidgets.QLineEdit()
    nombre_nuevo.setStyleSheet("background-color: white;")
    input_layout.addWidget(nombre_nuevo, alignment=Qt.AlignCenter)

    # Inputs Descipcion
    label_descripcion = QLabel("Descipcion")
    label_descripcion.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_descripcion, alignment=Qt.AlignCenter)
    descripcion_nueva = QtWidgets.QLineEdit()
    descripcion_nueva.setStyleSheet("background-color: white;")
    input_layout.addWidget(descripcion_nueva, alignment=Qt.AlignCenter)

    # Inputs Precio
    label_precio = QLabel("Precio")
    label_precio.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_precio, alignment=Qt.AlignCenter)
    precio_nuevo = QtWidgets.QLineEdit()
    precio_nuevo.setStyleSheet("background-color: white;")
    input_layout.addWidget(precio_nuevo, alignment=Qt.AlignCenter)

    # Inputs Ingredientes
    label_ingredientes = QLabel("Ingredientes")
    label_ingredientes.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_ingredientes, alignment=Qt.AlignCenter)
    ingredientes_nuevo = QtWidgets.QLineEdit()
    ingredientes_nuevo.setStyleSheet("background-color: white;")
    ingredientes_nuevo.setPlaceholderText("Ejemplo: tomate,2; lechuga,1; cebolla,3")  
    input_layout.addWidget(ingredientes_nuevo, alignment=Qt.AlignCenter)

    # Añade el layout de inputs al layout principal
    main_layout.addLayout(input_layout)

    # Añade el layout principal al frame
    frame.addLayout(main_layout)

    #Muestra los platos
    plato = Plato.mostrar_platos()
    table.setRowCount(len(plato))
    for row, admin in enumerate(plato):
        for col, value in enumerate(admin):
            table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    # Función para manejar la selección de la tabla
    def on_select():
        selected = table.selectedItems()
        if selected:
            id_ingresado.setText(selected[0].text())
            nombre_nuevo.setText(selected[1].text())
            descripcion_nueva.setText(selected[2].text())
            precio_nuevo.setText(selected[3].text())
            ingredientes_nuevo.setText(selected[4].text())

    table.itemSelectionChanged.connect(on_select)

# Crear un layout horizontal para los botones
    button_layout = QtWidgets.QHBoxLayout()

   # Botón para Añadir platos
    btn_añadir = diseño_boton("Añadir Plato")
    btn_añadir.clicked.connect(lambda: [Plato.agregar_plato(nombre_nuevo.text(), descripcion_nueva.text(), precio_nuevo.text(), ingredientes_nuevo.text()),actualizar_tabla(table,Plato.mostrar_platos)])               
    button_layout.addWidget(btn_añadir)

    #Boton para Modificar el Plato
    btn_modificar = diseño_boton("Modificar Plato")
    btn_modificar.clicked.connect(lambda: [Plato.modificar_plato(id_ingresado.text(),nombre_nuevo.text(), descripcion_nueva.text(), precio_nuevo.text(), ingredientes_nuevo.text()),actualizar_tabla(table,Plato.mostrar_platos)])
    button_layout.addWidget(btn_modificar)

    # Botón para eliminar el plato
    btn_eliminar = diseño_boton("Eliminar Plato")
    btn_eliminar.clicked.connect(lambda: [Plato.eliminar_plato(id_ingresado.text()),actualizar_tabla(table,Plato.mostrar_platos)])
    button_layout.addWidget(btn_eliminar)

    # Botón para volver al menu del admin
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: menu_admin(frame))
    button_layout.addWidget(boton_volver)

    # Añade el layout de botones debajo de la tabla
    frame.addLayout(button_layout)

    # Alinea el layout de botones al centro
    button_layout.setAlignment(Qt.AlignCenter)
        
#Pantalla editar ingredientes
def editar_ingredientes(frame):
    #Limpia pantalla
    limpiar_pantalla(frame)

    # Etiqueta de editar Ingrediente
    label_menu = QLabel("Editar Ingredientes")
    label_menu.setFont(QFont("Helvetica", 18, QFont.Bold))
    label_menu.setAlignment(Qt.AlignCenter)
    frame.addWidget(label_menu)

    # Crea una tabla
    table = QtWidgets.QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["ID","Nombre","Stock"])
    table.verticalHeader().setVisible(False)
    table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    # Ajustar el ancho de las columnas
    table.setColumnWidth(0, 100)   
    table.setColumnWidth(1, 300)  
    table.setColumnWidth(2, 400)   

    # Fija un tamaño mínimo para la tabla
    table.setMinimumSize(700, 250)

    # Hace que las columnas se ajusten automáticamente
    header = table.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    table.setStyleSheet("background: #FFDBB8;")

    # Crea un layout horizontal para la tabla y los inputs
    main_layout = QtWidgets.QHBoxLayout()

    # Añade la tabla al layout principal
    main_layout.addWidget(table, alignment=Qt.AlignCenter)

    # Crea un layout vertical para los labels y QLineEdits
    input_layout = QtWidgets.QVBoxLayout()

    # Inputs ID
    label_id = QLabel("ID")
    label_id.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_id, alignment=Qt.AlignCenter)
    id_ingresado = QtWidgets.QLineEdit()
    id_ingresado.setStyleSheet("background-color: white;")
    input_layout.addWidget(id_ingresado, alignment=Qt.AlignCenter)

    # Inputs nombre
    label_nombre = QLabel("Nombre")
    label_nombre.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_nombre, alignment=Qt.AlignCenter)
    nombre_nuevo = QtWidgets.QLineEdit()
    nombre_nuevo.setStyleSheet("background-color: white;")
    input_layout.addWidget(nombre_nuevo, alignment=Qt.AlignCenter)

    # Inputs Stock
    label_stock = QLabel("Stock")
    label_stock.setFont(QFont("Helvetica", 12, QFont.Bold))
    input_layout.addWidget(label_stock, alignment=Qt.AlignCenter)
    stock_nueva = QtWidgets.QLineEdit()
    stock_nueva.setStyleSheet("background-color: white;")
    input_layout.addWidget(stock_nueva, alignment=Qt.AlignCenter)

    # Añade el layout de inputs al layout principal
    main_layout.addLayout(input_layout)

    # Añade el layout principal al frame
    frame.addLayout(main_layout)

    #Muestra los ingredientes
    ingrediente = Ingredientes.mostrar_bd_Ingredientes()
    table.setRowCount(len(ingrediente))
    for row, ingre in enumerate(ingrediente):
        for col, value in enumerate(ingre):
            table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

    # Función para manejar la selección de la tabla
    def on_select():
        selected = table.selectedItems()
        if selected:
            id_ingresado.setText(selected[0].text())
            nombre_nuevo.setText(selected[1].text())
            stock_nueva.setText(selected[2].text())
            

    table.itemSelectionChanged.connect(on_select)

# Crear un layout horizontal para los botones
    button_layout = QtWidgets.QHBoxLayout()

    # Botón para Añadir Ingrediente
    btn_añadir = diseño_boton("Añadir \n Ingrediente")
    btn_añadir.clicked.connect(lambda: [Ingredientes.añadir_ingrediente(nombre_nuevo.text(),stock_nueva.text()), actualizar_tabla(table, Ingredientes.mostrar_bd_Ingredientes)])               
    button_layout.addWidget(btn_añadir)

    #Boton para Modificar el Ingrediente
    btn_modificar = diseño_boton("Modificar \n Ingrediente")
    btn_modificar.clicked.connect(lambda: [Ingredientes.modificar_ingrediente(id_ingresado.text(), nombre_nuevo.text(), stock_nueva.text()), actualizar_tabla(table, Ingredientes.mostrar_bd_Ingredientes)])
    button_layout.addWidget(btn_modificar)

    # Botón para eliminar ingrediente
    btn_eliminar = diseño_boton("Eliminar \n Ingrediente")
    btn_eliminar.clicked.connect(lambda: [Ingredientes.eliminar_ingrediente(id_ingresado.text()), actualizar_tabla(table, Ingredientes.mostrar_bd_Ingredientes)])
    button_layout.addWidget(btn_eliminar)

    # Botón para volver al menu del admin
    boton_volver = diseño_boton("Volver")
    boton_volver.clicked.connect(lambda: menu_admin(frame))
    button_layout.addWidget(boton_volver)

    # Añadir el layout de botones debajo de la tabla
    frame.addLayout(button_layout)

    # Alinear el layout de botones al centro
    button_layout.setAlignment(Qt.AlignCenter) 

# Creación de la ventana
def pantalla_principal():
    # Crear la aplicación
    app = QApplication(sys.argv)

    # Crear la ventana principal
    pantalla = QMainWindow()

    # Configuración de la ventana
    pantalla.setWindowTitle("Digital Order")
    pantalla.setWindowIcon(QIcon('Iconos\\DigitalOrder.png'))

    # Tamaño de la ventana
    ancho, alto = 800, 700

    # Centra la ventana en la pantalla
    ancho_pantalla = QApplication.primaryScreen().size().width()
    alto_pantalla = QApplication.primaryScreen().size().height()
    pos_x = (ancho_pantalla // 2) - (ancho // 2)
    pos_y = (alto_pantalla // 2) - (alto // 2)
    pantalla.setGeometry(pos_x, pos_y, ancho, alto)

    # Crea un widget central y un layout
    contenedor = QWidget()
    pantalla.setCentralWidget(contenedor)
    # Establece el color de fondo del contenedor
    contenedor.setStyleSheet("background-color: #d9b5a9;")
    frame = QVBoxLayout(contenedor)

    # Muestra la pantalla inicial
    pantalla_inicial(frame)

    # Muestra la ventana
    pantalla.show()

    # Ejecuta el bucle principal de la aplicación
    sys.exit(app.exec_())

# Llama a la función pantalla_principal para mostrar la ventana
pantalla_principal()