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

# Crear la tabla Pedido_Plato con la columna 'estado' ya incluida
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pedido_Plato (
    pedido_id INT,
    plato_id INT,
    cantidad INT NOT NULL DEFAULT 1,
    estado VARCHAR(255) DEFAULT 'Pendiente',
    PRIMARY KEY (pedido_id, plato_id),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (plato_id) REFERENCES platos(id)
)
''')

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS historial_pedido (
    pedido_id INT,
    plato_id INT,
    cantidad INT NOT NULL DEFAULT 1,
    estado VARCHAR(255) DEFAULT 'Pendiente',
    PRIMARY KEY (pedido_id, plato_id),
    FOREIGN KEY (pedido_id) REFERENCES pedido(id),
    FOREIGN KEY (plato_id) REFERENCES platos(id)
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

            # Sincronizar con historial_pedido
            cursor.execute("INSERT INTO historial_pedido (pedido_id, plato_id, cantidad, estado) VALUES (%s, %s, %s, 'Pendiente') ON DUPLICATE KEY UPDATE cantidad = cantidad + %s", 
                        (pedido_id, plato_id, cantidad, cantidad))
        
            conn.commit()
            print("Plato agregado o actualizado en el carrito.")
        else:
            print("Plato no encontrado en la base de datos.")
    # Cracion de excepciones para los posibles errores           
    except pymysql.MySQLError as e:
        print(f"Error en agregar_al_carrito: {e}")        


# Función para confirmar el pedido del carrito
def confirmar_pedido(pedido_id, numero_mesa):
    try:
        # Calcular el precio final sumando los precios de los platos en el pedido
        cursor.execute(""" 
            SELECT SUM(p.precio * pp.cantidad) 
            FROM Pedido_Plato pp 
            JOIN platos p ON pp.plato_id = p.id 
            WHERE pp.pedido_id=%s 
        """, (pedido_id,))
    
        resultado = cursor.fetchone()
        precio_final = resultado[0] if resultado else 0  

        # Actualiza el pedido con el número de mesa y el precio final
        cursor.execute("UPDATE pedido SET numeroMesa=%s, precioFinal=%s WHERE id=%s", (numero_mesa, precio_final, pedido_id))

        # Actualiza historial_pedido (opcional, dependiendo de cómo quieras manejarlo)
        cursor.execute("UPDATE historial_pedido SET estado = 'Confirmado' WHERE pedido_id = %s", (pedido_id,))
    
        conn.commit()
    
        return "Pedido confirmado y stock actualizado correctamente."
    # Cracion de excepciones para los posibles errores   
    except pymysql.MySQLError as e:
        print(f"Error en confirmar_pedido: {e}")


# Función que crea el carrito
def crear_carrito():
    try:
        # Pone en -1 el numeroMesa para crear un carrito temporal
        cursor.execute("SELECT id FROM pedido WHERE numeroMesa = -1")
        resultado = cursor.fetchone()

        # Verifica que exista un carrito temporal, sino crea uno
        if resultado:
            return resultado[0]
        else:
            cursor.execute("INSERT INTO pedido (numeroMesa, precioFinal) VALUES (%s, %s)", (-1, 0))
            conn.commit()
            return cursor.lastrowid
     # Cracion de excepciones para los posibles errores       
    except pymysql.MySQLError as e:
        print(f"Error en crear_carrito: {e}")    

# Función para eliminar un plato del carrito
def eliminar_del_carrito(pedido_id, plato_id):
    try:
        cursor.execute("DELETE FROM Pedido_Plato WHERE pedido_id=%s AND plato_id=%s", (pedido_id, plato_id))
        # Eliminar también de historial_pedido
        cursor.execute("DELETE FROM historial_pedido WHERE pedido_id=%s AND plato_id=%s", (pedido_id, plato_id))
        conn.commit()
    # Cracion de excepciones para los posibles errores   
    except pymysql.MySQLError as e:
        print(f"Error en eliminar_del_carrito: {e}")


# Función para mostrar la información de los platos que se agregaron al carrito 
def mostrar_carrito(pedido_id):
    try:
        cursor.execute("""
            SELECT p.id, p.nombre, p.precio, pp.cantidad 
            FROM Pedido_Plato pp
            JOIN platos p ON pp.plato_id = p.id
            WHERE pp.pedido_id=%s
        """, (pedido_id,))
        return cursor.fetchall()
    # Cracion de excepciones para los posibles errores  
    except pymysql.MySQLError as e:
        print(f"Error en mostrar_carrito: {e}")

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
    try:
        nueva_cantidad = cantidad_existente + 1
        cursor.execute("UPDATE Pedido_Plato SET cantidad=%s WHERE pedido_id=%s AND plato_id=%s", 
                    (nueva_cantidad, pedido_id, plato_id))
        conn.commit()
    # Cracion de excepciones para los posibles errores
    except pymysql.MySQLError as e:
        print(f"Error en aumentar_cantidad: {e}")
    

def ver_pedidos():
    try:
        cursor.execute('''
            SELECT pedido.id, pedido.numeroMesa, platos.nombre, Pedido_Plato.cantidad
            FROM pedido
            JOIN Pedido_Plato ON pedido.id = Pedido_Plato.pedido_id
            JOIN platos ON Pedido_Plato.plato_id = platos.id
        ''')
        
        pedidos = cursor.fetchall()
        pedidos_dict = {}
        for pedido_id, numero_mesa, nombre_plato, cantidad in pedidos:
            if pedido_id not in pedidos_dict:
                pedidos_dict[pedido_id] = {
                    'numero_mesa': numero_mesa,
                    'platos': []
                }
            pedidos_dict[pedido_id]['platos'].append({'nombre': nombre_plato, 'cantidad': cantidad})

        for pedido_id, detalles in pedidos_dict.items():
            print(f"Pedido ID: {pedido_id}, Mesa: {detalles['numero_mesa']}")
            for plato in detalles['platos']:
                print(f"  Plato: {plato['nombre']}, Cantidad: {plato['cantidad']}")
     # Cracion de excepciones para los posibles errores
    except pymysql.MySQLError as e:
        print(f"Error en ver_pedidos: {e}")            
                
def obtener_pedidos():
    cursor.execute('''
        SELECT pedido.id, pedido.numeroMesa, platos.nombre, Pedido_Plato.cantidad, Pedido_Plato.estado 
        FROM pedido 
        JOIN Pedido_Plato ON pedido.id = Pedido_Plato.pedido_id 
        JOIN platos ON Pedido_Plato.plato_id = platos.id
    ''')
    return cursor.fetchall()

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
            eliminar_pedido(pedido_id)
            return True 
        else:
            return False  

        cursor.execute("UPDATE Pedido_Plato SET estado = %s WHERE pedido_id = %s", (nuevo_estado, pedido_id))
        conn.commit()
    # Cracion de excepciones para los posibles errores
    except pymysql.MySQLError as e:
        print(f"Error en actualizar_estado: {e}")    

def eliminar_pedido(pedido_id):
    cursor.execute("DELETE FROM Pedido_Plato WHERE pedido_id = %s", (pedido_id,))
    cursor.execute("DELETE FROM pedido WHERE id = %s", (pedido_id,))
    conn.commit()
    print(f"Pedido {pedido_id} eliminado correctamente.")

def bloquear_mesa(mesa_id):
    try:
        cursor.execute("SELECT id FROM pedido WHERE numeroMesa = %s", (mesa_id,))
        pedido = cursor.fetchone()
        return pedido is not None
    # Cracion de excepciones para los posibles errores
    except pymysql.MySQLError as e:
        print(f"Error en la consulta: {e}")
        return False
