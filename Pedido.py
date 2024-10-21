import pymysql

# Conexión con la Base de Datos
conn = pymysql.connect( 
    host='26.92.40.13',
    user='root',
    password='',
    database='platos_bd'
)

cursor = conn.cursor()

# Crear las tablas si no existen
# Crear la tabla Platos
cursor.execute('''
CREATE TABLE IF NOT EXISTS platos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio FLOAT NOT NULL
)
''')

# Crear la tabla Pedidos
cursor.execute('''
CREATE TABLE IF NOT EXISTS pedido (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numeroMesa INT UNIQUE NOT NULL,
    precioFinal INTEGER NOT NULL
)
''')

#Crear la tabla Pedido_Plato
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pedido_Plato (
    pedido_id INT,
    plato_id INT,
    cantidad INT NOT NULL DEFAULT 1,
    PRIMARY KEY (pedido_id, plato_id),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (plato_id) REFERENCES platos(id)
)
''')

conn.commit()

def agregar_columna_estado():
    # Agregar la columna 'estado' con valor por defecto 'Pendiente'
    cursor.execute('''
        ALTER TABLE pedido_plato ADD COLUMN estado VARCHAR(255) DEFAULT 'Pendiente'
    ''')
    conn.commit()  # Confirma el cambio en la base de datos
    print("Columna 'estado' agregada correctamente.")

    # Actualizar todas las filas existentes para que tengan 'Pendiente' en la columna 'estado'
    cursor.execute('''
        UPDATE pedido_plato SET estado = 'Pendiente' WHERE estado IS NULL
    ''')
    conn.commit()  # Confirma el cambio
    print("Todas las filas actualizadas con el valor 'Pendiente'.")

# Funcion para agregar un plato al carrito
def agregar_al_carrito(pedido_id, nombre_plato, cantidad):
        #Busca la id del plato mediante su nombre
        cursor.execute("SELECT id FROM platos WHERE nombre = %s", (nombre_plato,))
        resultado = cursor.fetchone()

        if resultado:
            # Obtener la ID del plato
            plato_id = resultado[0]  
            
            # Verificar si el plato ya está en el carrito
            cursor.execute("SELECT cantidad FROM Pedido_Plato WHERE pedido_id = %s AND plato_id = %s", (pedido_id, plato_id))
            resultado_carrito = cursor.fetchone()

            if resultado_carrito:
                # Si ya está en el carrito, actualizar la cantidad
                nueva_cantidad = resultado_carrito[0] + cantidad
                cursor.execute("UPDATE Pedido_Plato SET cantidad = %s WHERE pedido_id = %s AND plato_id = %s", (nueva_cantidad, pedido_id, plato_id))
            else:
                # Si no está en el carrito, insertar el plato
                cursor.execute("INSERT INTO Pedido_Plato (pedido_id, plato_id, cantidad) VALUES (%s, %s, %s)", (pedido_id, plato_id, cantidad))

            print("Plato agregado o actualizado en el carrito.")
        else:
            print("Plato no encontrado en la base de datos.")

#Funcion para confirmar el pedido del carrito
def confirmar_pedido(pedido_id, numero_mesa):
    # Calcular el precio final sumando los precios de los platos en el pedido
    cursor.execute(""" 
        SELECT SUM(p.precio * pp.cantidad) 
        FROM Pedido_Plato pp 
        JOIN platos p ON pp.plato_id = p.id 
        WHERE pp.pedido_id=%s 
    """, (pedido_id,))
    
    resultado = cursor.fetchone()
    # Si no hay platos, precio_final será 0
    precio_final = resultado[0] if resultado else 0  

    # Obtener los ingredientes requeridos y sus cantidades para el pedido actual
    cursor.execute("""
        SELECT pi.ingrediente_id, SUM(pi.cantidad * pp.cantidad) AS total_cantidad
        FROM Plato_Ingredientes pi
        JOIN Pedido_Plato pp ON pi.plato_id = pp.plato_id
        WHERE pp.pedido_id = %s
        GROUP BY pi.ingrediente_id
    """, (pedido_id,))
    
    ingredientes_requeridos = cursor.fetchall()

    # Valida que haya suficiente stock para cada ingrediente
    for ingrediente_id, cantidad_requerida in ingredientes_requeridos:
        cursor.execute("SELECT stock FROM ingredientes WHERE id = %s", (ingrediente_id,))
        stock_actual = cursor.fetchone()[0]

        if stock_actual < cantidad_requerida:
            return f"No hay suficiente stock para el ingrediente ID {ingrediente_id}. Pedido no confirmado."

    # Si hay suficiente stock, resta los ingredientes
    for ingrediente_id, cantidad_requerida in ingredientes_requeridos:
        cursor.execute("UPDATE ingredientes SET stock = stock - %s WHERE id = %s", (cantidad_requerida, ingrediente_id))

    # Actualiza el pedido con el número de mesa y el precio final
    cursor.execute("UPDATE pedido SET numeroMesa=%s, precioFinal=%s WHERE id=%s", (numero_mesa, precio_final, pedido_id))
    conn.commit() 
    
    return "Pedido confirmado y stock actualizado correctamente."

#Funcion que crea el carrito
def crear_carrito():
    #Pone en -1 el numeroMesa para crear un carrito temporal
    cursor.execute("SELECT id FROM pedido WHERE numeroMesa = -1")
    resultado = cursor.fetchone()

    #Verifica que exista un carrito temporal, sino existe uno lo crea 
    if resultado:
        return resultado[0]
    else:
        cursor.execute("INSERT INTO pedido (numeroMesa, precioFinal) VALUES (%s, %s)", (-1, 0))
        conn.commit()
        return cursor.lastrowid

#Funcion para eliminar un plato del carrito
def eliminar_del_carrito(pedido_id, plato_id):
    cursor.execute("DELETE FROM Pedido_Plato WHERE pedido_id=%s AND plato_id=%s", (pedido_id, plato_id))
    conn.commit()

#Funcion para mostrar la informacio de los platos que se agregaron al carrito 
def mostrar_carrito(pedido_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.nombre, p.precio, pp.cantidad 
        FROM Pedido_Plato pp
        JOIN platos p ON pp.plato_id = p.id
        WHERE pp.pedido_id=%s
    """, (pedido_id,))
    return cursor.fetchall() 

#Funcion para reducir la cantidad de un plato dento del carrito, si la cantidad llega a 0 lo elimina 
def reducir_cantidad(cantidad_exitente, pedido_id, plato_id):
    if cantidad_exitente > 0:
        reducir = 1
        nueva_cantidad = cantidad_exitente - reducir
        if cantidad_exitente == 0:
             cursor.execute("DELETE FROM Pedido_Plato WHERE pedido_id=%s AND plato_id=%s", (pedido_id, plato_id))
             conn.commit()
        else:
             cursor = conn.cursor()
             cursor.execute("UPDATE Pedido_Plato SET cantidad=%s WHERE pedido_id=%s AND plato_id=%s", 
                           (nueva_cantidad, pedido_id, plato_id))
             conn.commit()

#Funcion para aumentar la cantidad de un plato dento del carrito
def aumentar_cantidad(cantidad_exitente, pedido_id, plato_id):
    aumentar = 1 
    nueva_cantidad = cantidad_exitente + aumentar
    cursor.execute("UPDATE Pedido_Plato SET cantidad=%s WHERE pedido_id=%s AND plato_id=%s", 
                           (nueva_cantidad, pedido_id, plato_id))
    conn.commit()


def ver_pedidos():
    # Unir las tablas pedido y Pedido_Plato para obtener la información completa
    cursor.execute('''
        SELECT pedido.id, pedido.numeroMesa, platos.nombre, Pedido_Plato.cantidad
        FROM pedido
        JOIN Pedido_Plato ON pedido.id = Pedido_Plato.pedido_id
        JOIN platos ON Pedido_Plato.plato_id = platos.id
    ''')
    
    pedidos = cursor.fetchall()

    # Creamos un diccionario para organizar la información por pedido
    pedidos_dict = {}
    for pedido_id, numero_mesa, nombre_plato, cantidad in pedidos:
        if pedido_id not in pedidos_dict:
            pedidos_dict[pedido_id] = {
                'numero_mesa': numero_mesa,
                'platos': []
            }
        pedidos_dict[pedido_id]['platos'].append({'nombre': nombre_plato, 'cantidad': cantidad})

    # Mostrar los pedidos de manera organizada
    for pedido_id, detalles in pedidos_dict.items():
        print(f"Pedido ID: {pedido_id}, Mesa: {detalles['numero_mesa']}")
        for plato in detalles['platos']:
            print(f"  Plato: {plato['nombre']}, Cantidad: {plato['cantidad']}")
            
def obtener_pedidos():
        cursor.execute('''
        SELECT pedido.id, pedido.numeroMesa, platos.nombre, pedido_plato.cantidad, pedido_plato.estado 
        FROM pedido 
        JOIN pedido_plato ON pedido.id = pedido_plato.pedido_id 
        JOIN platos ON pedido_plato.plato_id = platos.id
''')
        return cursor.fetchall()

    
def actualizar_estado(pedido_id):
    try:
        # Obtener el estado actual del pedido
        cursor.execute("SELECT estado FROM pedido_plato WHERE pedido_id = %s", (pedido_id,))
        estado_actual = cursor.fetchone()[0]
    except(TypeError,IndexError):
        print(f"No se encontro el pedido con ID {pedido_id}.")
        return False   
   
    # Verificar el estado y actualizar
    if estado_actual == "Pendiente":
        nuevo_estado = "En preparación"
    elif estado_actual == "En preparación":
        nuevo_estado = "Listo"
    elif estado_actual == "Listo":
        # Si el estado ya está en "Listo", elimina el pedido
        eliminar_pedido(pedido_id)
        return True  # Salir ya que se eliminó el pedido
    else:
        return False  # No se hace nada si no es un estado válido

    # Actualizar el estado en la tabla
    cursor.execute("UPDATE pedido_plato SET estado = %s WHERE pedido_id = %s", (nuevo_estado, pedido_id))
    conn.commit()

    # Si el pedido llega al estado "Listo", eliminarlo
    if nuevo_estado == "Listo":
        eliminar_pedido(pedido_id)

    return True

def eliminar_pedido(pedido_id):
    # Primero eliminamos de Pedido_Plato las entradas asociadas al pedido
    cursor.execute("DELETE FROM pedido_plato WHERE pedido_id = %s", (pedido_id,))
    conn.commit()

    # Luego eliminamos el pedido de la tabla pedido
    cursor.execute("DELETE FROM pedido WHERE id = %s", (pedido_id,))
    conn.commit()

    print(f"Pedido {pedido_id} eliminado correctamente.")

def bloquear_mesa(mesa_id):
    try:
        #Este metodo sirve para que cuando una mesa tenga un pedido se bloquee los btn
        cursor.execute(f'''SELECT id FROM pedido WHERE numeroMesa = {mesa_id} ''') 
        pedido = cursor.fetchone()
        return pedido is not None
    except pymysql.MySQLError as e:
            print(f"Error en la consulta: {e}")
            return False


          
         


    
