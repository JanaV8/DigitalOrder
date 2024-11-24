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

# Crear la tabla Pedidos sin restricción UNIQUE en numeroMesa
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS pedido (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numeroMesa INT NOT NULL,
    precioFinal INTEGER NOT NULL,
    estado ENUM('activo', 'completado', 'cancelado') DEFAULT 'activo'
)
''')

# Crear la tabla Pedido_Plato
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS Pedido_Plato (
    pedido_id INT,
    plato_id INT,
    cantidad INT NOT NULL DEFAULT 1,
    estado VARCHAR(255) DEFAULT 'Pendiente',
    estado VARCHAR(255) DEFAULT 'Pendiente',
    PRIMARY KEY (pedido_id, plato_id),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (plato_id) REFERENCES platos(id)
)
''')

# Crear la tabla Historial_Pedido_Plato sin FOREIGN KEY
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS historial_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    plato_id INT NOT NULL,
    cantidad INT DEFAULT 1,
    estado VARCHAR(20) DEFAULT 'Confirmado'
)
''')

conn.commit()

# Función para agregar un plato al carrito
def agregar_al_carrito(pedido_id, nombre_plato, cantidad):
    try:
        # Busca la ID del plato mediante su nombre
        cursor.execute("SELECT id FROM platos WHERE nombre = %s", (nombre_plato,))
        resultado = cursor.fetchone()

        if resultado:
            plato_id = resultado[0]
            cursor.execute("SELECT cantidad FROM Pedido_Plato WHERE pedido_id = %s AND plato_id = %s", (pedido_id, plato_id))
            resultado_carrito = cursor.fetchone()

            if resultado_carrito:
                nueva_cantidad = resultado_carrito[0] + cantidad
                cursor.execute("UPDATE Pedido_Plato SET cantidad = %s WHERE pedido_id = %s AND plato_id = %s", (nueva_cantidad, pedido_id, plato_id))
            else:
                cursor.execute("INSERT INTO Pedido_Plato (pedido_id, plato_id, cantidad) VALUES (%s, %s, %s)", (pedido_id, plato_id, cantidad))

            # Se inserta en el historial sin restricciones
            cursor.execute("INSERT INTO historial_pedido (pedido_id, plato_id, cantidad, estado) VALUES (%s, %s, %s, 'Confirmado')", (pedido_id, plato_id, cantidad))

            conn.commit()
            print("Plato agregado o actualizado en el carrito y sincronizado en historial_pedido.")
        else:
            print("Plato no encontrado en la base de datos.")
    # Cracion de excepciones para los posibles errores 
    except pymysql.MySQLError as e:
        print(f"Error en reducir_cantidad: {e}")
       
# Función para confirmar el pedido del carrito
def confirmar_pedido(pedido_id, numero_mesa):
    # Verificar si hay un pedido activo con el mismo numeroMesa
    cursor.execute("SELECT id FROM pedido WHERE numeroMesa=%s AND estado='activo'", (numero_mesa,))
    if cursor.fetchone():
        print("Ya hay un pedido activo para esta mesa.")
        return

    # Calcular el precio total del pedido
    cursor.execute(""" 
        SELECT SUM(p.precio * pp.cantidad)
        FROM Pedido_Plato pp
        JOIN platos p ON pp.plato_id = p.id
        WHERE pp.pedido_id=%s
    """, (pedido_id,))

    resultado = cursor.fetchone()
    precio_final = resultado[0] if resultado else 0

    # Actualizar el estado del pedido y el precio final
    cursor.execute("UPDATE pedido SET numeroMesa=%s, precioFinal=%s, estado='completado' WHERE id=%s", (numero_mesa, precio_final, pedido_id))

    # Copiar los datos de Pedido_Plato a historial_pedido
    cursor.execute('''
        INSERT INTO historial_pedido (pedido_id, plato_id, cantidad, estado)
        SELECT pedido_id, plato_id, cantidad, estado
        FROM Pedido_Plato
        WHERE pedido_id = %s
    ''', (pedido_id,))

    conn.commit()
    print("Pedido confirmado y completado.")

# Función para crear un nuevo pedido
def crear_pedido(numero_mesa):
    # Verificar si hay un pedido activo para esa mesa
    cursor.execute("SELECT id FROM pedido WHERE numeroMesa=%s AND estado='activo'", (numero_mesa,))
    if cursor.fetchone():
        print("Ya hay un pedido activo para esta mesa.")
        return

    cursor.execute("INSERT INTO pedido (numeroMesa, precioFinal) VALUES (%s, 0)", (numero_mesa,))
    conn.commit()
    print("Pedido creado con éxito.")

# Función que crea el carrito
def crear_carrito():
    cursor.execute("SELECT id FROM pedido WHERE numeroMesa = -1")
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]
    else:
        cursor.execute("INSERT INTO pedido (numeroMesa, precioFinal) VALUES (%s, %s)", (-1, 0))
        conn.commit()
        return cursor.lastrowid

# Función para eliminar un plato del carrito
def eliminar_del_carrito(pedido_id, plato_id):
    cursor.execute("DELETE FROM Pedido_Plato WHERE pedido_id=%s AND plato_id=%s", (pedido_id, plato_id))
    cursor.execute("DELETE FROM historial_pedido WHERE pedido_id=%s AND plato_id=%s", (pedido_id, plato_id))
    conn.commit()

# Función para mostrar la información de los platos que se agregaron al carrito 
def mostrar_carrito(pedido_id):
    cursor.execute(""" 
        SELECT p.id, p.nombre, p.precio, pp.cantidad 
        FROM Pedido_Plato pp 
        JOIN platos p ON pp.plato_id = p.id 
        WHERE pp.pedido_id=%s 
    """, (pedido_id,))
    return cursor.fetchall()

# Función para reducir la cantidad de un plato en el carrito; si la cantidad llega a 0 lo elimina 
def reducir_cantidad(cantidad_existente, pedido_id, plato_id):
    try:
        reducir = 1
        nueva_cantidad = cantidad_existente - reducir
        if nueva_cantidad <= 0:
            cursor.execute("DELETE FROM Pedido_Plato WHERE pedido_id=%s AND plato_id=%s", (pedido_id, plato_id))
        else:
            cursor.execute("UPDATE Pedido_Plato SET cantidad=%s WHERE pedido_id=%s AND plato_id=%s", 
                        (nueva_cantidad, pedido_id, plato_id))
        conn.commit()
    # Cracion de excepciones para los posibles errores 
    except pymysql.MySQLError as e:
        print(f"Error en reducir_cantidad: {e}")
    
# Función para aumentar la cantidad de un plato en el carrito
def aumentar_cantidad(cantidad_existente, pedido_id, plato_id):
    nueva_cantidad = cantidad_existente + 1
    cursor.execute("UPDATE Pedido_Plato SET cantidad=%s WHERE pedido_id=%s AND plato_id=%s", 
                   (nueva_cantidad, pedido_id, plato_id))
    conn.commit()

# Obtener todos los pedidos
def obtener_pedidos():
    cursor.execute(''' 
        SELECT pedido.id, pedido.numeroMesa, platos.nombre, Pedido_Plato.cantidad, Pedido_Plato.estado 
        FROM pedido 
        JOIN Pedido_Plato ON pedido.id = Pedido_Plato.pedido_id 
        JOIN platos ON Pedido_Plato.plato_id = platos.id 
    ''')
    return cursor.fetchall()

# Obtener el historial de pedidos sin depender de la tabla pedido
def obtener_historial():
    try:
        cursor.execute('''
        SELECT 
            historial_pedido.pedido_id, 
            historial_pedido.plato_id, 
            platos.nombre, 
            SUM(historial_pedido.cantidad) AS total_cantidad
        FROM historial_pedido
        JOIN platos ON historial_pedido.plato_id = platos.id
        GROUP BY historial_pedido.pedido_id, historial_pedido.plato_id, platos.nombre
        ORDER BY historial_pedido.pedido_id DESC
    ''')
        return cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error al obtener el historial de pedidos: {e}")
        return []

# Actualizar el estado de un pedido
def actualizar_estado(pedido_id):
    try:
        cursor.execute("SELECT estado FROM Pedido_Plato WHERE pedido_id = %s", (pedido_id,))
        resultado = cursor.fetchone()
        if resultado:
            estado_actual = resultado[0]
        else:
            print(f"No se encontró el pedido con ID {pedido_id}.")
            return False   

        # Verificar el estado y actualizar
        if estado_actual == "Pendiente":
            nuevo_estado = "En preparación"
        elif estado_actual == "En preparación":
            nuevo_estado = "Listo"
        elif estado_actual == "Listo":
               
            return True 
        else:
            return False  

        cursor.execute("UPDATE Pedido_Plato SET estado = %s WHERE pedido_id = %s", (nuevo_estado, pedido_id))
        conn.commit()
        # Cracion de excepciones para los posibles errores
    except pymysql.MySQLError as e:
        print(f"Error en actualizar_estado: {e}")    

# Eliminar un pedido
def eliminar_pedido(pedido_id):
    try:
        # Primero eliminamos los platos asociados al pedido
        cursor.execute("DELETE FROM Pedido_Plato WHERE pedido_id = %s", (pedido_id,))
        conn.commit()

        # Ahora eliminamos el pedido de la tabla principal
        cursor.execute("DELETE FROM pedido WHERE id = %s", (pedido_id,))
        conn.commit()
        
        print(f"Pedido {pedido_id} eliminado de la tabla pedido y de Pedido_Plato.")
    except pymysql.MySQLError as e:
        print(f"Error al eliminar el pedido: {e}")

def bloquear_mesa(mesa_id):
    try:
        cursor.execute("SELECT id FROM pedido WHERE numeroMesa = %s", (mesa_id,))
        pedido = cursor.fetchone()
        return pedido is not None
    # Cracion de excepciones para los posibles errores
    except pymysql.MySQLError as e:
        print(f"Error en la consulta: {e}")