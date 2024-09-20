import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

# Función para mostrar el menú de platos después de seleccionar la mesa
def mostrarMenu(frame, mesa_seleccionada):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Etiqueta para indicar la mesa seleccionada
    label_menu = ttk.Label(frame, text=f"Menú para la Mesa {mesa_seleccionada}", font=("Helvetica", 18, "bold"), foreground="#E0E0E0", background="#333333")
    label_menu.pack(pady=10)

    # Lista de platos (a modo de ejemplo)
    platos = [("Ensalada", 5.00), ("Pancho", 3.50), ("Pizza", 8.00), ("Choripan", 7.50), ("Hamburguesa", 6.00)]
    
    # Variable para almacenar el precio total
    total = tk.DoubleVar(value=0.0)
    
    # Función para agregar el precio del plato seleccionado
    def agregarPlato(precio):
        total.set(total.get() + precio)

    # Mostrar los platos en forma de botones
    for plato, precio in platos:
        boton_plato = ttk.Button(frame, text=f"{plato} - ${precio:.2f}", style="DarkButton.TButton", 
                                 command=lambda p=precio: agregarPlato(p))
        boton_plato.pack(pady=5)
    
    # Mostrar el total acumulado
    etiqueta_total = ttk.Label(frame, text="Total acumulado:", font=("Helvetica", 14), foreground="#E0E0E0", background="#333333")
    etiqueta_total.pack(pady=10)

    etiqueta_total_valor = ttk.Label(frame, textvariable=total, font=("Helvetica", 14, "bold"), foreground="#E0E0E0", background="#333333")
    etiqueta_total_valor.pack(pady=10)

# Función para mostrar las mesas disponibles
def seleccionarMesa(frame):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Etiqueta de instrucción
    label_mesas = ttk.Label(frame, text="Selecciona una mesa:", font=("Helvetica", 18, "bold"), foreground="#E0E0E0", background="#333333")
    label_mesas.pack(pady=10)

    # Crear un frame para contener los botones de mesas
    mesas_frame = ttk.Frame(frame, padding="10", style="TFrame")
    mesas_frame.pack(expand=True)

    # Crear botones para hasta 20 mesas en una cuadrícula
    for i in range(1, 21):
        boton_mesa = ttk.Button(mesas_frame, text=f"Mesa {i}", style="DarkButton.TButton", 
                                command=lambda i=i: mostrarMenu(frame, i))
        boton_mesa.grid(row=(i-1)//5, column=(i-1)%5, padx=10, pady=10)

# Función para mostrar la pantalla inicial con el botón "Seleccionar Mesa"
def pantallaInicial(frame):
    # Limpiar el frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Etiqueta de bienvenida
    label = ttk.Label(frame, text="Digital Order", font=("Helvetica", 24, "bold"), foreground="#E0E0E0", background="#333333")
    label.pack(pady=10)

    # Botón para seleccionar mesa
    button = ttk.Button(frame, text="Seleccionar Mesa", style="DarkButton.TButton", command=lambda: seleccionarMesa(frame))
    button.pack(pady=20, padx=20)

# Función para la pantalla principal
def pantallaPrincipal():
    pantalla = tk.Tk()  # Crear ventana principal
    pantalla.iconphoto(False, PhotoImage(file='DigitalOrder.png'))  # Icono de la Aplicación
    pantalla.title("Digital Order")  # Título Principal
    window_width = 600  # Ancho de la ventana
    window_height = 480  # Alto de la ventana

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

    # Estilo moderno en modo oscuro
    style = ttk.Style()
    style.theme_create("darkmode", parent="alt", settings={
        "TLabel": {"configure": {"font": ("Helvetica", 14), "background": "#333333", "foreground": "#E0E0E0"}},
        "DarkButton.TButton": {
            "configure": {"font": ("Helvetica", 12), "padding": 10, "relief": "flat", 
                          "background": "#444444", "foreground": "#E0E0E0", "borderwidth": 0,
                          "focuscolor": ""},
            "map": {
                "background": [("active", "#555555"), ("pressed", "#222222")],
                "foreground": [("active", "#E0E0E0"), ("pressed", "#E0E0E0")]
            }
        },
        "TFrame": {"configure": {"background": "#333333"}}
    })
    style.theme_use("darkmode")

    # Mostrar pantalla inicial con el botón "Seleccionar Mesa"
    pantallaInicial(frame)

    pantalla.mainloop()

pantallaPrincipal()
