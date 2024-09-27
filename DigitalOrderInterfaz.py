import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import Administrador
import pymysql

# Funcion para limpiar la pantalla (Elimina todos los widgets)
def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Pantalla de Selección de Mesas
def seleccionar_mesa(frame):
    #Limpia la pantalla
    limpiar_frame(frame)
    
    #Etiqueta de seleccion de mesa
    ttk.Label(frame, text="Selecciona una mesa:", font=("Helvetica", 18, "bold"), 
              foreground="#E0E0E0", background="#333333").pack(pady=10)

    mesas_frame = ttk.Frame(frame, padding="10", style="TFrame")
    mesas_frame.pack(expand=True)
    
    #Crea 20 mesas
    for i in range(1, 21):
        ttk.Button(mesas_frame, text=f"Mesa {i}", style="DarkButton.TButton", 
                   command=lambda i=i: mostrar_menu(frame, i)).grid(row=(i-1)//4, column=(i-1)%4, padx=10, pady=10)

    #Boton para volver Atras
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: pantalla_inicial(frame)).pack(pady=10)
    
# Pantalla de Menú de Platos
def mostrar_menu(frame, mesa_seleccionada):
    #Limpia la Pantalla
    limpiar_frame(frame)

    #Etiqueta del menu para la mesa seleccionada
    ttk.Label(frame, text=f"Menú para la Mesa {mesa_seleccionada}", 
              font=("Helvetica", 18, "bold"), foreground="#E0E0E0", 
              background="#333333").pack(pady=10)

    #Creacion de Menu (Provicional)
    platos = [("Empanada", 700), ("Pancho", 4000), ("Pizza", 8000), 
              ("Choripan", 6000), ("Hamburguesa", 7000)]
    total = tk.DoubleVar(value=0.0)

    #Funcion para agregar Platos a la orden
    def agregar_plato(precio):
        total.set(total.get() + precio)
    for plato, precio in platos:
        ttk.Button(frame, text=f"{plato} - ${precio:.2f}", 
                   style="DarkButton.TButton", 
                   command=lambda p=precio: agregar_plato(p)).pack(pady=5, padx=10, fill='x')

    #Etiqueta con el precio total del pedido
    ttk.Label(frame, text="Total de su Pedido:", 
              font=("Helvetica", 14), foreground="#E0E0E0", 
              background="#333333").pack(pady=10)

    ttk.Label(frame, textvariable=total, 
              font=("Helvetica", 14, "bold"), foreground="#E0E0E0", 
              background="#333333").pack(pady=10)

    #Boton para confirmar el pedido
    ttk.Button(frame, text="Confirmar Pedido", style="DarkButton.TButton", 
               command=lambda: confirmar_pedido(frame, mesa_seleccionada, total.get())).pack(pady=20)

    #Boton para volver atras
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: seleccionar_mesa(frame)).pack(pady=10)

#Funcion para confirmar el pedido
def confirmar_pedido(frame, mesa_seleccionada, total):
    #Limpia la pantalla
    limpiar_frame(frame)

    #Muestra por pantalla el pedido confirmado para la mesa y su total
    mensaje = f"Pedido confirmado para la Mesa {mesa_seleccionada}, Total: ${total:.2f}"
    ttk.Label(frame, text=mensaje, font=("Helvetica", 18, "bold"), 
              foreground="#E0E0E0", background="#333333").pack(pady=20)

# Pantalla de Inicio de Sesión
def iniciar_sesion(frame, rol):
    #Limpia la pantalla
    limpiar_frame(frame)

    #Etiqueta para iniciar Sesion
    ttk.Label(frame, text=f"Iniciar sesión ({rol})", font=("Helvetica", 18, "bold")).pack(pady=10)

    #Etiqueta Usuario
    ttk.Label(frame, text="Usuario:").pack(pady=5)
    
    #Se guarda el valor de la variable
    entry_usuario = ttk.Entry(frame)
    entry_usuario.pack(pady=5)

    #Etiqueta Contraseña
    ttk.Label(frame, text="Contraseña:").pack(pady=5)
    
    entry_contraseña = ttk.Entry(frame, show="*")
    entry_contraseña.pack(pady=5)

    ttk.Button(frame, text="Mostrar Contraseña", style="DarkButton.TButton", 
               command=lambda: mostrar_contraseña(entry_contraseña)).pack(pady=10)

    ttk.Button(frame, text="Iniciar sesión", style="DarkButton.TButton", 
               command=lambda: confirmar_login(entry_usuario, entry_contraseña, frame)).pack(pady=10)

    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: pantalla_inicial(frame)).pack(pady=10)

def confirmar_login(entry_usuario, entry_contraseña, frame):
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
            
    if not usuario or not contraseña:
        ttk.Label(frame, text="Usuario y/o contraseña vacíos", foreground="red").pack(pady=5)
    else:
        islogin = Administrador.validarAdministrador(usuario, contraseña)
        if islogin == True:
            mostrar_menu_admin(frame)  # Cambiar a una pantalla de administrador
        else:
            ttk.Label(frame, text="Usuario y/o contraseña incorrectos", foreground="red").pack(pady=5)

#Funcion para mostrar u ocultar la contraseña
def mostrar_contraseña(entry):
    if entry.cget("show") == "*":
        entry.config(show="")
    else:
        entry.config(show="*")

#Funcion para mostrar el menu una vez ingreso el administrador
def mostrar_menu_admin(frame):
    limpiar_frame(frame)

    ttk.Label(frame, text="Panel de Administración", font=("Helvetica", 18, "bold"), 
              foreground="#E0E0E0", background="#333333").pack(pady=10)

    # Botón para Agregar Administrador
    ttk.Button(frame, text="Agregar Administrador", style="DarkButton.TButton", 
               command=lambda: pantalla_agregar_admin(frame)).pack(pady=10)

    # Botón para Eliminar Administrador
    ttk.Button(frame, text="Eliminar Administrador", style="DarkButton.TButton", 
               command=lambda: pantalla_eliminar_admin(frame)).pack(pady=10)

    # Botón para Editar Menú 
    ttk.Button(frame, text="Editar Menú", style="DarkButton.TButton", 
               command=lambda: pantalla_editar_menu(frame)).pack(pady=10)

    # Botón para Editar Ingredientes 
    ttk.Button(frame, text="Editar Ingredientes", style="DarkButton.TButton", 
               command=lambda: pantalla_editar_ingredientes(frame)).pack(pady=10)

    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: pantalla_inicial(frame)).pack(pady=10)

# Pantalla para editar el menú
def pantalla_editar_menu(frame):
    limpiar_frame(frame)

    ttk.Label(frame, text="Editar Menú", font=("Helvetica", 18, "bold"), 
              foreground="#E0E0E0", background="#333333").pack(pady=10)

    # Botón para Añadir Plato
    ttk.Button(frame, text="Añadir Plato", style="DarkButton.TButton", 
               command=lambda: Administrador.añadir_plato(frame)).pack(pady=10)

    # Botón para Modificar Plato
    ttk.Button(frame, text="Modificar Plato", style="DarkButton.TButton", 
               command=lambda: Administrador.modificar_plato(frame)).pack(pady=10)

    # Botón para Eliminar Plato
    ttk.Button(frame, text="Eliminar Plato", style="DarkButton.TButton", 
               command=lambda: Administrador.eliminar_plato(frame)).pack(pady=10)

    # Botón para Volver al panel de administración
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: mostrar_menu_admin(frame)).pack(pady=10)

# Pantalla para editar ingredientes
def pantalla_editar_ingredientes(frame):
    limpiar_frame(frame)

    ttk.Label(frame, text="Editar Ingredientes", font=("Helvetica", 18, "bold"), 
              foreground="#E0E0E0", background="#333333").pack(pady=10)

    # Botón para Añadir Ingrediente
    ttk.Button(frame, text="Añadir Ingrediente", style="DarkButton.TButton", 
               command=lambda: Administrador.añadir_ingrediente(frame)).pack(pady=10)

    # Botón para Modificar Ingrediente
    ttk.Button(frame, text="Modificar Ingrediente", style="DarkButton.TButton", 
               command=lambda: Administrador.modificar_ingrediente(frame)).pack(pady=10)

    # Botón para Eliminar Ingrediente
    ttk.Button(frame, text="Eliminar Ingrediente", style="DarkButton.TButton", 
               command=lambda: Administrador.eliminar_ingrediente(frame)).pack(pady=10)

    # Botón para Volver al panel de administración
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: mostrar_menu_admin(frame)).pack(pady=10)

def pantalla_agregar_admin(frame):
    limpiar_frame(frame)

    # Título de la pantalla
    ttk.Label(frame, text="Agregar Nuevo Administrador", font=("Helvetica", 18, "bold"), 
              foreground="#E0E0E0", background="#333333").pack(pady=10)

    # Etiqueta de Usuario
    ttk.Label(frame, text="Usuario:").pack(pady=5)
    entry_usuario = ttk.Entry(frame)
    entry_usuario.pack(pady=5)

    # Etiqueta de Contraseña
    ttk.Label(frame, text="Contraseña:").pack(pady=5)
    entry_contraseña = ttk.Entry(frame, show="*")
    entry_contraseña.pack(pady=5)

    # Botón para agregar el administrador
    ttk.Button(frame, text="Agregar", style="DarkButton.TButton", 
               command=lambda: agregar_admin(entry_usuario.get(), entry_contraseña.get(), frame)).pack(pady=10)

    # Botón para volver al menú anterior
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: mostrar_menu_admin(frame)).pack(pady=10)

# Función para agregar administrador
def agregar_admin(usuario, contraseña, frame):
    # Validar que los campos no estén vacíos
    if not usuario or not contraseña:
        ttk.Label(frame, text="Usuario y/o contraseña vacíos", foreground="red").pack(pady=5)
    else:
        # Intentar agregar al administrador
        mensaje = Administrador.agregarAdministrador(usuario, contraseña)
        ttk.Label(frame, text=mensaje, foreground="green" if "Correctamente" in mensaje else "red").pack(pady=5)

def pantalla_eliminar_admin(frame):
    limpiar_frame(frame)

    ttk.Label(frame, text="Eliminar Administrador", font=("Helvetica", 18, "bold"), 
              foreground="#E0E0E0", background="#333333").pack(pady=10)

    ttk.Label(frame, text="Usuario:").pack(pady=5)
    entry_usuario = ttk.Entry(frame)
    entry_usuario.pack(pady=5)

    ttk.Button(frame, text="Eliminar", style="DarkButton.TButton", 
               command=lambda: eliminar_admin(entry_usuario.get(), frame)).pack(pady=10)

    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: mostrar_menu_admin(frame)).pack(pady=10)

def eliminar_admin(usuario, frame):
    mensaje = Administrador.eliminarAdministrador(usuario)
    ttk.Label(frame, text=mensaje, foreground="green" if "exitosamente" in mensaje else "red").pack(pady=5)

# Pantalla Inicial
def pantalla_inicial(frame):
    limpiar_frame(frame)

    ttk.Label(frame, text="Digital Order", font=("Helvetica", 24, "bold"), 
              foreground="#E0E0E0", background="#333333").pack(pady=10)

     # Cargar la imagen de fondo para el botón
    fondo_boton = PhotoImage(file="Digital Order\Iconos\Fondo Boton.png")

    # Crear un botón con la imagen de fondo
    tk.Button(frame, text="Seleccionar Mesa", image=fondo_boton, compound="center", 
              font=("Helvetica", 14, "bold"), fg="#E0E0E0", bg="#333333", 
              command=lambda: seleccionar_mesa(frame)).pack(pady=20)

    # Mantener la referencia de la imagen
    frame.image = fondo_boton

    ttk.Button(frame, text="Iniciar sesión (Admin)", style="DarkButton.TButton", 
               command=lambda: iniciar_sesion(frame, "Admin")).pack(pady=10)

    ttk.Button(frame, text="Iniciar sesión (Cocinero)", style="DarkButton.TButton", 
               command=lambda: iniciar_sesion(frame, "Cocinero")).pack(pady=10)

# Configuración de la ventana principal
def pantalla_principal():
    # Código para agregar un administrador por defecto
    usuario_inicial = "AdminPrincipal"
    contraseña_inicial = "1234"
    mensaje = Administrador.agregarAdministrador(usuario_inicial, contraseña_inicial)
    print(mensaje)  # Esto imprimirá si el administrador fue agregado correctamente o si ya existe.


    pantalla = tk.Tk()
    pantalla.iconphoto(False, PhotoImage(file='Digital Order\Iconos\DigitalOrder.png'))  # Manteniendo el icono
    pantalla.title("Digital Order")
    
    # Centrando la ventana
    window_width, window_height = 600, 580
    screen_width, screen_height = pantalla.winfo_screenwidth(), pantalla.winfo_screenheight()
    position_x, position_y = (screen_width // 2) - (window_width // 2), (screen_height // 2) - (window_height // 2)
    pantalla.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Frame principal y estilo
    frame = ttk.Frame(pantalla, padding="20")
    frame.pack(expand=True, fill="both")

    estilo_moderno(frame)

    pantalla_inicial(frame)
    pantalla.mainloop()

def estilo_moderno(frame):
    style = ttk.Style()
    style.theme_create("darkmode", parent="alt", settings={
        "TLabel": {"configure": {"font": ("Helvetica", 14), "background": "#333333", "foreground": "#E0E0E0"}},
        "DarkButton.TButton": {
            "configure": {"font": ("Helvetica", 14), "padding": (10, 5), "relief": "flat", 
                          "background": "#444444", "foreground": "#E0E0E0", "borderwidth": 0},
            "map": {
                "background": [("active", "#555555"), ("pressed", "#222222")],
                "foreground": [("active", "#E0E0E0"), ("pressed", "#E0E0E0")]
            }
        },
        "TFrame": {"configure": {"background": "#333333"}}
    })
    style.theme_use("darkmode")

pantalla_principal()