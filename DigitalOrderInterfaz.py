import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

# Función para mostrar el menú de platos después de seleccionar la mesa
def mostrarMenu(frame, mesa_seleccionada):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Etiqueta para indicar la mesa seleccionada
    label_menu = ttk.Label(frame, text=f"Menú para la Mesa {mesa_seleccionada}", font=("Helvetica", 18, "bold"))
    label_menu.pack(pady=10)

    # Lista de platos (a modo de ejemplo)
    platos = [("Ensalada", 5.00), ("Sopa", 3.50), ("Pizza", 8.00), ("Pasta", 7.50), ("Hamburguesa", 6.00)]
    
    # Variable para almacenar el precio total
    total = tk.DoubleVar(value=0.0)
    
    # Función para agregar el precio del plato seleccionado
    def agregarPlato(precio):
        total.set(total.get() + precio)

    # Mostrar los platos en forma de botones
    for plato, precio in platos:
        boton_plato = ttk.Button(frame, text=f"{plato} - ${precio:.2f}", style="TButton", 
                                 command=lambda p=precio: agregarPlato(p))
        boton_plato.pack(pady=5)
    
    # Mostrar el total acumulado
    etiqueta_total = ttk.Label(frame, text="Total acumulado:", font=("Helvetica", 14))
    etiqueta_total.pack(pady=10)

    etiqueta_total_valor = ttk.Label(frame, textvariable=total, font=("Helvetica", 14, "bold"))
    etiqueta_total_valor.pack(pady=10)

# Función para mostrar las mesas disponibles
def seleccionarMesa(frame):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Etiqueta de instrucción
    label_mesas = ttk.Label(frame, text="Selecciona una mesa:", font=("Helvetica", 18, "bold"))
    label_mesas.grid(row=0, column=0, columnspan=5, pady=10)

    # Crear botones para hasta 20 mesas en una cuadrícula
    for i in range(1, 21):
        boton_mesa = ttk.Button(frame, text=f"Mesa {i}", style="TButton", 
                                command=lambda i=i: mostrarMenu(frame, i))
        boton_mesa.grid(row=(i-1)//5 + 1, column=(i-1)%5, padx=10, pady=10)

# Función para mostrar la pantalla inicial con el botón "Seleccionar Mesa"
def pantallaInicial(frame):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Etiqueta de bienvenida
    label = ttk.Label(frame, text="Digital Order", font=("Helvetica", 24, "bold"), padding="10")
    label.pack(pady=10)

    # Botón para seleccionar mesa
    button = ttk.Button(frame, text="Seleccionar Mesa", style="TButton", command=lambda: seleccionarMesa(frame))
    button.pack(pady=20, padx=20)

# Función para la pantalla principal
def pantallaPrincipal():
    pantalla = tk.Tk()  # Crear ventana principal
    pantalla.iconphoto(False, PhotoImage(file='DigitalOrder.png'))  # Icono de la Aplicación
    pantalla.title("Digital Order")  # Título Principal
    window_width = 600  # Ancho de la ventana
    window_height = 400  # Alto de la ventana

    # Obtener la resolución de la pantalla
    screen_width = pantalla.winfo_screenwidth()
    screen_height = pantalla.winfo_screenheight()

    # Calcular el centro de la pantalla
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    pantalla.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")  # Ajustar el tamaño y la posición de la ventana

    # Crear un frame para actualizar los contenidos
    frame = ttk.Frame(pantalla, padding="20")
    frame.pack(expand=True, fill="both")

    # Estilo del botón
    style = ttk.Style()
    style.theme_create("modern", parent="alt", settings={
        "TLabel": {"configure": {"font": ("Helvetica", 14), "background": "#f0f0f0"}},
        "TButton": {"configure": {"font": ("Helvetica", 12), "background": "#4CAF50", "foreground": "white"}},
        "TFrame": {"configure": {"background": "#f0f0f0"}}
    })
    style.theme_use("modern")
    style.configure("TButton", font=("Helvetica", 12), padding=10, relief="flat", background="#4CAF50")
    style.map("TButton", background=[("active", "#45a049"), ("pressed", "#357a38")])  # Efecto al pasar el mouse

    # Mostrar pantalla inicial con el botón "Seleccionar Mesa"
    pantallaInicial(frame)

    pantalla.mainloop()

pantallaPrincipal()