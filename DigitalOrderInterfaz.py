import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import Administrador
import Ingredientes
import Plato
import Pedido


#Funcion para limpiar la pantalla (Elimina todos los widgets)
def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

#Pantalla de Selección de Mesas
def seleccionar_mesa(frame):
    #Limpia la pantalla
    limpiar_frame(frame)
    
    #Etiqueta de seleccion de mesa
    ttk.Label(frame, text="Selecciona una mesa:", font=("Helvetica", 18, "bold"), 
              foreground="#000000", background="#d9b5a9").pack(pady=10)

    #Crea un frame para contener todos los botones de la mesa
    mesas_frame = ttk.Frame(frame, padding="10", style="TFrame")
    mesas_frame.pack(expand=True)
    
    #Crea 20 mesas
    for i in range(1, 21):
        ttk.Button(mesas_frame, text=f"Mesa {i}", style="DarkButton.TButton", 
                   command=lambda i=i: mostrar_menu(frame, i)).grid(row=(i-1)//4, column=(i-1)%4, padx=10, pady=10)
        

    #Boton para volver Atras
    ttk.Button(frame, text="Volver", style="DarkButton.TButton",
               command=lambda: pantalla_inicial(frame)).pack(pady=10)
    
def mostrar_menu(frame, mesa_seleccionada):
    # Limpia la Pantalla
    limpiar_frame(frame)
    
    # Crea el carrito para el pedido
    pedido_id = Pedido.crear_carrito()
    
    # Etiqueta del menu para la mesa seleccionada
    ttk.Label(frame, text=f"Menú para la Mesa {mesa_seleccionada}", 
              font=("Helvetica", 18, "bold"), foreground="#000000", 
              background="#d9b5a9").pack(pady=10)

    # Botón para ver el carrito
    ttk.Button(frame, text="Carrito", 
           command=lambda: mostrar_carrito_interfaz(frame, pedido_id,mesa_seleccionada)).pack(pady=10)  # Cambia la llamada aquí

    # Menú de platos
    platos = Plato.mostrar_platos()
    for idx, (plato_id, nombre, descripcion, precio) in enumerate(platos):
        ttk.Label(frame, text=f"{nombre} - {descripcion} - ${precio}").pack()  # Cambia grid() por pack()
        ttk.Button(frame, text="Agregar al carrito", 
           command=lambda p_id=plato_id: Pedido.agregar_al_carrito(pedido_id, p_id, 1)).pack()  # Cambia grid() por pack()

    # Botón para volver atrás
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: seleccionar_mesa(frame)).pack(pady=10)



def mostrar_carrito_interfaz(frame, pedido_id,mesa_seleccionada):
    # Limpia la pantalla
    limpiar_frame(frame)

    # Etiqueta para mostrar el carrito
    ttk.Label(frame, text="Carrito", font=("Helvetica", 18, "bold")).pack(pady=10)

    # Obtener los elementos del carrito
    items = Pedido.mostrar_carrito(pedido_id)

    # Mostrar los elementos en el carrito
    for plato_id, nombre, precio, cantidad in items:
        ttk.Label(frame, text=f"{nombre} - ${precio} x {cantidad}").pack(pady=5)
        
        # Aquí 'plato_id' ya está definido desde la consulta
        ttk.Button(frame, text="Eliminar", command=lambda p_id=plato_id: Pedido.eliminar_del_carrito(pedido_id, p_id)).pack(pady=5)

    # Botón para confirmar el pedido
    ttk.Button(frame, text="Confirmar Pedido", command=lambda: Pedido.confirmar_pedido(pedido_id,mesa_seleccionada)).pack(pady=10)
    
    # Botón para volver
    ttk.Button(frame, text="Volver", command=lambda: mostrar_menu(frame, -1)).pack(pady=10)

#Pantalla de Inicio de Sesión
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

    #Muestra la contraseña si lo requiere el usuario
    entry_contraseña = ttk.Entry(frame, show="*")
    entry_contraseña.pack(pady=5)

    #Boton Mostrar contraseña
    ttk.Button(frame, text="Mostrar Contraseña", style="DarkButton.TButton", 
               command=lambda: mostrar_contraseña(entry_contraseña)).pack(pady=10)

    #Boton para Iniciar Sesion
    ttk.Button(frame, text="Iniciar Sesión", style="DarkButton.TButton", 
               command=lambda: confirmar_login(entry_usuario, entry_contraseña, frame)).pack(pady=10)

    #Boton para volver atras
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: pantalla_inicial(frame)).pack(pady=10)

#Funcion para Confirmar el Inicio de Sesion
def confirmar_login(entry_usuario, entry_contraseña, frame):
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    #Si el usuario y/o contraseña son vacios o son incorrectos se imprimen en la pantalla
    if not usuario or not contraseña:
        ttk.Label(frame, text="Usuario y/o contraseña vacíos", foreground="red").pack(pady=5)
    else:
        islogin = Administrador.validarAdministrador(usuario, contraseña)
        if islogin == True:
            mostrar_menu_admin(frame)  # Cambiar a una pantalla de administrador
        else:
            ttk.Label(frame, text="Usuario y/o contraseña incorrectos", foreground="red").pack(pady=5)

#Funcion para Mostrar u Ocultar la contraseña
def mostrar_contraseña(entry):
    if entry.cget("show") == "*":
        entry.config(show="")
    else:
        entry.config(show="*")

#Funcion para Mostrar el Menu una vez Ingresa el Administrador
def mostrar_menu_admin(frame):
    #Limpia la pantalla
    limpiar_frame(frame)

    #Etiqueta Con el menu del administrador
    ttk.Label(frame, text="Panel de Administración", font=("Helvetica", 18, "bold"), 
              foreground="#000000", background="#d9b5a9").pack(pady=10)

    # Botón para Agregar Administrador
    ttk.Button(frame, text="Agregar Administrador", style="DarkButton.TButton", 
               command=lambda: pantalla_agregar_admin(frame)).pack(pady=10)

    #Boton para modificar datos de administrador
    ttk.Button(frame, text="Modificar Administrador", style="DarkButton.TButton", 
               command=lambda: pantalla_modificar_admin(frame)).pack(pady=10)

    # Botón para Editar Menú 
    ttk.Button(frame, text="Editar Menú", style="DarkButton.TButton", 
               command=lambda: pantalla_editar_menu(frame)).pack(pady=10)

    # Botón para Editar Ingredientes 
    ttk.Button(frame, text="Editar Ingredientes", style="DarkButton.TButton", 
               command=lambda: pantalla_editar_ingredientes(frame)).pack(pady=10)

    #Boton para volver atras
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: pantalla_inicial(frame)).pack(pady=10)

#Pantalla para Editar el Menú
def pantalla_editar_menu(frame):
    # Limpia la Pantalla
    limpiar_frame(frame)

    # Etiqueta para editar el menu (Administrador)
    ttk.Label(frame, text="Editar Menú", font=("Helvetica", 18, "bold"), 
              foreground="#000000", background="#d9b5a9").pack(pady=10)

    # Crear scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical")

    # Crear Treeview para mostrar platos
    tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Descripcion", "Precio"), show='headings')
    style_treeview(tree)
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Descripcion", text="Descripcion")
    tree.heading("Precio", text="Precio")

    # Empaquetar el Treeview y el scrollbar uno al lado del otro
    tree.pack(side="left", fill="both", expand=True, pady=10)
    scrollbar.pack(side="left", fill="y")

    # Asociar scrollbar al Treeview
    scrollbar.config(command=tree.yview)

    # Cargar platos en el Treeview
    Lista_platos = Plato.mostrar_platos()
    for b_platos in Lista_platos:
        tree.insert("", "end", values=b_platos)

    # Función para llenar los campos de entrada al seleccionar un plato
    def on_select(event):
        selected_item = tree.selection()[0]  # Obtiene el item seleccionado
        id_pl = tree.item(selected_item, "values")[0]
        nombre_pl = tree.item(selected_item, "values")[1]
        descripcion_pl = tree.item(selected_item, "values")[2]
        precio_pl = tree.item(selected_item, "values")[3]

        id.delete(0, tk.END)
        id.insert(0, id_pl)
        nombre.delete(0, tk.END)
        nombre.insert(0, nombre_pl)
        descripcion.delete(0, tk.END) 
        descripcion.insert(0, descripcion_pl)
        precio.delete(0, tk.END)
        precio.insert(0, precio_pl)

    tree.bind("<<TreeviewSelect>>", on_select)

    # Etiquetas y campos de entrada
    ttk.Label(frame, text="ID:").pack(pady=5)
    id = ttk.Entry(frame)
    id.pack(pady=5)

    ttk.Label(frame, text="Nombre:").pack(pady=5)
    nombre = ttk.Entry(frame)
    nombre.pack(pady=5)

    ttk.Label(frame, text="Descripcion:").pack(pady=5)
    descripcion = ttk.Entry(frame)
    descripcion.pack(pady=5)

    ttk.Label(frame, text="Precio:").pack(pady=5)
    precio = ttk.Entry(frame)
    precio.pack(pady=5)

    # Etiqueta y campo para ingresar ingredientes
    ttk.Label(frame, text="Ingredientes (nombre,cantidad):").pack(pady=5)
    ingredientes = ttk.Entry(frame)
    ingredientes.pack(pady=5)

    # Botón para Añadir Plato 
    ttk.Button(frame, text="Añadir Plato", style="DarkButton.TButton", 
               command=lambda: [agregar_plato(nombre.get(), descripcion.get(), precio.get(), ingredientes.get()), 
                            actualizar_treeview(tree,Plato.mostrar_platos)]).pack(pady=10)

    # Botón para Modificar Plato 
    ttk.Button(frame, text="Modificar Plato", style="DarkButton.TButton", 
               command=lambda: [Plato.modificar_plato(id.get() or None, nombre.get() or None, descripcion.get() or None, precio.get() or None, ingredientes.get() or None), 
                            actualizar_treeview(tree,Plato.mostrar_platos)]).pack(pady=10)

    # Botón para Eliminar Plato
    ttk.Button(frame, text="Eliminar Plato", style="DarkButton.TButton", 
               command=lambda: [Plato.eliminar_plato(id.get()), 
                            actualizar_treeview(tree,Plato.mostrar_platos)]).pack(pady=10)

    # Botón para Volver atras
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: mostrar_menu_admin(frame)).pack(pady=10)

def agregar_plato(nombre, descripcion, precio, ingredientes_str):
    # Convertir el string de ingredientes a una lista de tuplas
    ingredientes = []
    for ing in ingredientes_str.split(","):
        nombre_ingrediente, cantidad = ing.split(":")  # Asegúrate de usar un formato consistente
        ingredientes.append((nombre_ingrediente.strip(), float(cantidad.strip())))  # Convertir a float

    resultado = Plato.agregar_plato(nombre, descripcion, precio, ingredientes)
    return resultado

#Pantalla para Editar Ingredientes
def pantalla_editar_ingredientes(frame):
    # Limpia la Pantalla
    limpiar_frame(frame)

    # Etiqueta Editar ingredientes
    ttk.Label(frame, text="Editar Ingredientes", font=("Helvetica", 18, "bold"), 
              foreground="#000000", background="#d9b5a9").pack(pady=10)

    # Crear scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical")

    # Crear Treeview para mostrar ingredientes
    tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Stock"), show='headings')
    style_treeview(tree)
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Stock", text="Stock")

    # Empaquetar el Treeview y el scrollbar uno al lado del otro
    tree.pack(side="left", fill="both", expand=True, pady=10)
    scrollbar.pack(side="left", fill="y")

    # Asociar scrollbar al Treeview
    scrollbar.config(command=tree.yview)

    # Cargar ingredientes en el Treeview
    Lista_ingredientes = Ingredientes.mostrar_BD_Ingredientes()
    for b_ingrediente in Lista_ingredientes:
        tree.insert("", "end", values=b_ingrediente)

    # Función para llenar los campos de entrada al seleccionar un ingrediente
    def on_select(event):
        selected_item = tree.selection()[0]  # Obtiene el item seleccionado
        id_ing = tree.item(selected_item, "values")[0]
        nombre_ing = tree.item(selected_item, "values")[1]
        stock_ing = tree.item(selected_item, "values")[2]

        id.delete(0, tk.END)
        id.insert(0, id_ing)
        nombre.delete(0, tk.END)
        nombre.insert(0, nombre_ing)
        cantidad.delete(0, tk.END) 
        cantidad.insert(0, stock_ing)

    tree.bind("<<TreeviewSelect>>", on_select)

     # Etiqueta de ID ingrediente
    ttk.Label(frame, text="ID:").pack(pady=5)
    id = ttk.Entry(frame)
    id.pack(pady=5)

    # Etiqueta de Nombre ingrediente
    ttk.Label(frame, text="Nombre:").pack(pady=5)
    nombre = ttk.Entry(frame)
    nombre.pack(pady=5)

    # Etiqueta de Stock ingrediente
    ttk.Label(frame, text="Cantidad:").pack(pady=5)
    cantidad = ttk.Entry(frame)
    cantidad.pack(pady=5)

    # Botón para Añadir Ingrediente
    ttk.Button(frame, text="Añadir Ingrediente", style="DarkButton.TButton", 
               command=lambda: [Ingredientes.añadir_ingrediente(nombre.get(), cantidad.get()),
                                actualizar_treeview(tree, Ingredientes.mostrar_BD_Ingredientes)]).pack(pady=10)

    # Botón para Modificar Ingrediente
    ttk.Button(frame, text="Modificar Ingrediente", style="DarkButton.TButton", 
               command=lambda: [Ingredientes.modificar_ingrediente(id.get(), nombre.get(), cantidad.get()),
                                actualizar_treeview(tree, Ingredientes.mostrar_BD_Ingredientes)]).pack(pady=10)

    # Botón para Eliminar Ingrediente
    ttk.Button(frame, text="Eliminar Ingrediente", style="DarkButton.TButton", 
               command=lambda: [Ingredientes.eliminar_ingrediente(id.get()),
                                actualizar_treeview(tree, Ingredientes.mostrar_BD_Ingredientes)]).pack(pady=10)

    # Botón para Volver al panel de administración
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: mostrar_menu_admin(frame)).pack(pady=10)

#Pantalla Agregar Admin
def pantalla_agregar_admin(frame):
    #Limpia la pantalla
    limpiar_frame(frame)

    # Etiqueta Agregar un nuevo administrador
    ttk.Label(frame, text="Agregar Nuevo Administrador", font=("Helvetica", 18, "bold"), 
              foreground="#000000", background="#d9b5a9").pack(pady=10)

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

#Función para Agregar Administrador
def agregar_admin(usuario, contraseña, frame):
    # Validar que los campos no estén vacíos
    if not usuario or not contraseña:
        ttk.Label(frame, text="Usuario y/o contraseña vacíos", foreground="red").pack(pady=5)
    else:
        # Etiqueta que muestra se agrega correctamente un administrador
        mensaje = Administrador.agregarAdministrador(usuario, contraseña)
        ttk.Label(frame, text=mensaje, foreground="green" if "Correctamente" in mensaje else "red").pack(pady=5)

#Funcion para Eliminar un Administrador
def eliminar_admin(id, frame):
    mensaje = Administrador.eliminarAdministrador(id)

    #etiqueta que muestra en color verde que se elimino correctamente
    ttk.Label(frame, text=mensaje, foreground="green" if "exitosamente" in mensaje else "red").pack(pady=5)

#Pantalla para Modificar los Datos del Administrador
def pantalla_modificar_admin(frame):
    #Limpia la pantalla
    limpiar_frame(frame)
    
    #Etiqueta para Modificar el administrador
    ttk.Label(frame, text="Modificar Administrador", font=("Helvetica", 18, "bold"), 
              foreground="#000000", background="#d9b5a9").pack(pady=10)
    
    # Crear scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical")

    # Crear Treeview para mostrar administradores
    tree = ttk.Treeview(frame, columns=("ID", "Usuario", "Contraseña"), show='headings')
    style_treeview(tree)
    tree.heading("ID", text="ID")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Contraseña", text="Contraseña")
    tree.pack(pady=10)

    # Empaquetar el Treeview y el scrollbar uno al lado del otro
    tree.pack(side="left", fill="both", expand=True, pady=10)
    scrollbar.pack(side="left", fill="y")

    # Asociar scrollbar al Treeview
    scrollbar.config(command=tree.yview)

    # Cargar administradores en el Treeview
    administradores = Administrador.obtener_administradores()
    for admin in administradores:
        tree.insert("", "end", values=admin)

    # Función para llenar los campos de entrada al seleccionar un administrador
    def on_select(event):
        selected_item = tree.selection()[0]  # Obtiene el item seleccionado
        id_admin, usuario, contraseña_existente = tree.item(selected_item, "values")
        id_ingresado.delete(0, tk.END)
        id_ingresado.insert(0, id_admin)
        nombre_nuevo.delete(0, tk.END)
        nombre_nuevo.insert(0, usuario)
        contraseña_nueva.delete(0, tk.END) 
        contraseña_nueva.insert(0, contraseña_existente) 

    tree.bind("<<TreeviewSelect>>", on_select)

    #Etiqueta para Ingresar el ID del Administrador
    ttk.Label(frame, text="Ingresar ID:").pack(pady=5)
    id_ingresado = ttk.Entry(frame)
    id_ingresado.pack(pady=5)
    
    #Etiqueta para ingresar el Nuevo nombre del Administrador
    ttk.Label(frame, text="Ingresar nuevo nombre:").pack(pady=5)
    nombre_nuevo = ttk.Entry(frame)
    nombre_nuevo.pack(pady=5)
    
    #Etiqueta para ingresar la nueva contraseña del Administrador
    ttk.Label(frame, text="Ingresar nueva contraseña:").pack(pady=5)
    contraseña_nueva = ttk.Entry(frame)
    contraseña_nueva.pack(pady=5)
    
    #Boton para modificar los datos ingresados
    ttk.Button(frame, text="Modificar", style="DarkButton.TButton", 
               command=lambda: [mod_admin(id_ingresado.get(), nombre_nuevo.get(), contraseña_nueva.get()), 
                            actualizar_treeview(tree, Administrador.obtener_administradores)]).pack(pady=10)
    
    #Boton para eliminar al administrador
    ttk.Button(frame, text="Eliminar", style="DarkButton.TButton",
               command=lambda: [eliminar_admin(id_ingresado.get(), frame),
                                actualizar_treeview(tree, Administrador.obtener_administradores)]).pack(pady=10)

    #Boton para volver atras
    ttk.Button(frame, text="Volver", style="DarkButton.TButton", 
               command=lambda: mostrar_menu_admin(frame)).pack(pady=10)

#Funcion para Modificar Administrador
def mod_admin(id_ingresado, nombre_nuevo, contraseña_nueva):
    Administrador.actualizarAdministrador(id_ingresado, nombre_nuevo, contraseña_nueva)
   
#Pantalla Inicial
def pantalla_inicial(frame):
    #Limpia la patalla
    limpiar_frame(frame)

    #Etiqueta con el titulo de la app
    ttk.Label(frame, text="Digital Order", font=("Helvetica", 24, "bold"), 
              foreground="#000000", background="#d9b5a9").pack(pady=10)

    # Fondo para el botón
    fondo_boton = PhotoImage(file="Iconos\\Fondo Boton.png")

    # Botón Seleccionar Mesa
    tk.Button(frame, text="Seleccionar Mesa", image=fondo_boton, compound="center",
          font=("Helvetica", 13, "bold"), fg="#ffffff", bg="#d9b5a9",
          borderwidth=0, highlightthickness=0,  
          activebackground="#d9b5a9", activeforeground="#000000", 
          command=lambda: seleccionar_mesa(frame)).pack(pady=10)

    # Botón Iniciar sesión (Admin)
    tk.Button(frame, text="Iniciar sesión Admin", image=fondo_boton, compound="center",
              font=("Helvetica", 13, "bold"), fg="#ffffff", bg="#d9b5a9",
              borderwidth=0, highlightthickness=0,
              activebackground="#d9b5a9", activeforeground="#000000", 
              command=lambda: iniciar_sesion(frame, "Admin")).pack(pady=10)

    # Botón Iniciar sesión (Cocinero)
    tk.Button(frame, text="Iniciar sesión Cocinero", image=fondo_boton, compound="center",
              font=("Helvetica", 11, "bold"), fg="#ffffff", bg="#d9b5a9",
              borderwidth=0, highlightthickness=0,
              activebackground="#d9b5a9", activeforeground="#000000", 
              command=lambda: iniciar_sesion(frame, "Cocinero")).pack(pady=10)

   # Cargar la imagen y redimensionarla
    imagen_original = Image.open("Iconos\\Chef.png")
    imagen_redimensionada = imagen_original.resize((300, 300), Image.LANCZOS)  # Cambia el tamaño aquí
    imagen_final = ImageTk.PhotoImage(imagen_redimensionada)

    # Crear un label para mostrar la imagen redimensionada
    ttk.Label(frame, image=imagen_final, background="#d9b5a9").pack(pady=20)

    # Mantener la referencia de las imágenes
    frame.image = fondo_boton
    frame.imagen_final = imagen_final

#Configuración de la ventana principal
def pantalla_principal():
    # Código para agregar un administrador por defecto
    usuario_inicial = "AdminPrincipal"
    contraseña_inicial = "1234"
    Administrador.agregarAdministrador(usuario_inicial, contraseña_inicial)

    #Crea la pantalla Princial
    pantalla = tk.Tk()

    #Icono de la aplicacion
    pantalla.iconphoto(False, PhotoImage(file='Iconos\\DigitalOrder.png'))  

    #Titulo de la app en la pantalla principal
    pantalla.title("Digital Order")
    
    #Crea la medida de la ventana
    window_width, window_height = 700, 680

    #Toma la resolucion de la pantalla donde se ejecuta y aparece en el centro de la pantalla
    screen_width, screen_height = pantalla.winfo_screenwidth(), pantalla.winfo_screenheight()
    position_x, position_y = (screen_width // 2) - (window_width // 2), (screen_height // 2) - (window_height // 2)
    pantalla.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    #Crear un marco en la ventana
    frame = ttk.Frame(pantalla, padding="20")
    frame.pack(expand=True, fill="both")

    #Llama a la funcion estilo moderno para que se aplique en la pantalla
    estilo_moderno(frame)

    #Muestra la pantalla incial
    pantalla_inicial(frame)

    #Ejecutar el bucle principal de la aplicación      
    pantalla.mainloop()

#Funcion para actualizar el TreeView
def actualizar_treeview(tree, obtener_datos_func):
    # Limpiar Treeview
    for item in tree.get_children():
        tree.delete(item)
    # Obtener nuevos datos y actualizar el Treeview
    datos = obtener_datos_func()
    for dato in datos:
        tree.insert("", "end", values=dato)

#Crea un estilo para aplicar en todas las pantallas
def estilo_moderno(frame):
    style = ttk.Style()
    style.theme_create("darkmode", parent="alt", settings={
        "TLabel": {
            "configure": {"font": ("Calibri", 14), "background": "#d9b5a9", "foreground": "#000000"}
        },
        "ModernButton.TButton": {
            "configure": {"font": ("Calibri", 16), "padding": (15, 10), "relief": "flat", 
                          "background": "#8C6A58", "foreground": "#ffffff", "borderwidth": 0},
            "map": {
                "background": [("active", "#b48776"), ("pressed", "#754f3e")],
                "foreground": [("active", "#ffffff"), ("pressed", "#ffffff")]
            }
        },
        "TFrame": {"configure": {"background": "#d9b5a9"}}
    })
    style.theme_use("darkmode")

#Crea estilo para el TreeView
def style_treeview(tree):
    style = ttk.Style()
    style.configure("Treeview",
                    background="#F5F5DC",  # Fondo del Treeview
                    foreground="#333333",  # Color del texto
                    rowheight=25,
                    fieldbackground="#F5F5DC")  # Fondo de las celdas

    style.map("Treeview",
              background=[("selected", "#007FFF")],  # Color cuando seleccionas
              foreground=[("selected", "#FFFFFF")])  # Color del texto cuando seleccionas

    # Estilo para los encabezados
    style.configure("Treeview.Heading",
                    background="#FFA500",  # Fondo naranja para encabezados
                    foreground="#FFFFFF",  # Texto blanco
                    font=("Helvetica", 13, "bold"))

    # Estilos para filas alternas
    style.configure("evenrow", background="#E6E6FA")  # Lavanda para filas pares
    style.configure("oddrow", background="#FFFFFF")    # Blanco para filas impares

#Fin de la pantalla
pantalla_principal()