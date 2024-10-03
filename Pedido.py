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
# Crear la tabla 'pedido'
cursor.execute('''
CREATE TABLE IF NOT EXISTS pedido (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numeroMesa INT UNIQUE NOT NULL,
    precioFinal INTEGER NOT NULL
)
''')

# Crear la tabla 'platos'
cursor.execute('''
CREATE TABLE IF NOT EXISTS platos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio FLOAT NOT NULL
)
''')

# Crear la tabla 'Pedido_Plato'
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

# Funcionalidad para que el cliente pueda guardar el pedido
def agregar_al_carrito(pedido_id, plato_id, cantidad):
    cursor.execute("SELECT cantidad FROM Pedido_Plato WHERE pedido_id=%s AND plato_id=%s", (pedido_id, plato_id))
    resultado = cursor.fetchone()
    
    if resultado:
        nueva_cantidad = resultado[0] + cantidad
        cursor.execute("UPDATE Pedido_Plato SET cantidad=%s WHERE pedido_id=%s AND plato_id=%s", (nueva_cantidad, pedido_id, plato_id))
    else:
        cursor.execute("INSERT INTO Pedido_Plato (pedido_id, plato_id, cantidad) VALUES (%s, %s, %s)", (pedido_id, plato_id, cantidad))
    
    conn.commit()

def confirmar_pedido(pedido_id, numero_mesa):
    # Calcular el precio final sumando los precios de los platos en el pedido
    cursor.execute(""" 
        SELECT SUM(p.precio * pp.cantidad) 
        FROM Pedido_Plato pp 
        JOIN platos p ON pp.plato_id = p.id 
        WHERE pp.pedido_id=%s 
    """, (pedido_id,))
    
    resultado = cursor.fetchone()
    precio_final = resultado[0] if resultado else 0  # Si no hay platos, precio_final será 0

    # Actualizar el pedido con el número de mesa y el precio final
    cursor.execute("UPDATE pedido SET numeroMesa=%s, precioFinal=%s WHERE id=%s", (numero_mesa, precio_final, pedido_id))
    conn.commit()  # Guardar los cambios en la base de datos


def crear_carrito():
    cursor.execute("SELECT id FROM pedido WHERE numeroMesa = -1")
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]
    else:
        cursor.execute("INSERT INTO pedido (numeroMesa, precioFinal) VALUES (%s, %s)", (-1, 0))
        conn.commit()
        return cursor.lastrowid

def eliminar_del_carrito(pedido_id, plato_id):
    cursor.execute("DELETE FROM Pedido_Plato WHERE pedido_id=%s AND plato_id=%s", (pedido_id, plato_id))
    conn.commit()

def mostrar_carrito(pedido_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.nombre, p.precio, pp.cantidad 
        FROM Pedido_Plato pp
        JOIN platos p ON pp.plato_id = p.id
        WHERE pp.pedido_id=%s
    """, (pedido_id,))
    return cursor.fetchall()  # Esto ahora retornará (plato_id, nombre, precio, cantidad)

