import pymysql

conn = pymysql.connect( 
        host='26.92.40.13',
        user='root',
        password='',
        database='platos_bd')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS platos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio FLOAT NOT NULL
)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Plato_Ingredientes (
        plato_id INTEGER,
        ingrediente_id INTEGER,
        cantidad REAL NOT NULL,
        FOREIGN KEY (plato_id) REFERENCES Platos (id),
        FOREIGN KEY (ingrediente_id) REFERENCES Ingredientes (id),
        PRIMARY KEY (plato_id, ingrediente_id )
    )
''')

conn.commit()

def mostrar_platos():
    # Consulta para obtener los platos junto con sus ingredientes y cantidades
    query = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, 
               GROUP_CONCAT(CONCAT(i.nombre, ' (', pi.cantidad, ')') SEPARATOR ', ') AS ingredientes
        FROM platos p
        LEFT JOIN Plato_Ingredientes pi ON p.id = pi.plato_id
        LEFT JOIN ingredientes i ON pi.ingrediente_id = i.id
        GROUP BY p.id
    """
    cursor.execute(query)
    Lista_platos = cursor.fetchall()
    return Lista_platos

#Funcion para mostrar el menu al cliente
def mostrar_menu ():
    cursor.execute("SELECT nombre, descripcion, precio FROM platos")
    Lista_menu = cursor.fetchall()
    return Lista_menu

def mostrar_ingredientes ():
    cursor.execute("SELECT nombre,cantidad WHERE ingrediente_id FROM ingredientes")
    Lista_menu = cursor.fetchall()
    return Lista_menu

def agregar_plato(nombre, descripcion, precio, ingredientes_str):
    # Insertar el nuevo plato
    cursor.execute("INSERT INTO platos (nombre, descripcion, precio) VALUES (%s, %s, %s)", (nombre, descripcion, precio))
    plato_id = cursor.lastrowid  # Obtener el ID del plato recién agregado

    # Separar el string de ingredientes en partes
    ingredientes = ingredientes_str.split(';') if ingredientes_str else []

    for ingrediente in ingredientes:
        # Separar nombre y cantidad
        if ',' in ingrediente:
            nombre_ingrediente, cantidad = ingrediente.split(',', 1)  # Limitar a 1 separación
            nombre_ingrediente = nombre_ingrediente.strip()  # Eliminar espacios
            cantidad = cantidad.strip()

            # Buscar el ID del ingrediente basado en su nombre
            cursor.execute("SELECT id FROM ingredientes WHERE nombre = %s", (nombre_ingrediente,))
            resultado = cursor.fetchone()

            if resultado:  # Si se encontró el ingrediente
                ingrediente_id = resultado[0]  # Obtener el ID
                cursor.execute("INSERT INTO Plato_Ingredientes (plato_id, ingrediente_id, cantidad) VALUES (%s, %s, %s)", (plato_id, ingrediente_id, cantidad))
            else:
                return f"Ingrediente '{nombre_ingrediente}' no existe. El plato no fue agregado."
        else:
            return "Formato incorrecto para el ingrediente. Debe ser 'nombre,cantidad'."

    # Confirmar cambios
    conn.commit()
    return "Plato agregado exitosamente."


def eliminar_plato(plato_id):
    # Primero, eliminamos los ingredientes asociados
    cursor.execute("DELETE FROM Plato_Ingredientes WHERE plato_id = %s", (plato_id,))
    
    # Luego, eliminamos el plato
    cursor.execute("DELETE FROM platos WHERE id = %s", (plato_id,))
    conn.commit()
    
    return "Plato eliminado correctamente." if cursor.rowcount > 0 else "El plato no existe."

def modificar_plato(plato_id, nuevo_nombre, nueva_descripcion, nuevo_precio, nuevos_ingredientes):
    # Actualizar los datos del plato
    if nuevo_nombre is not None or nueva_descripcion is not None or nuevo_precio is not None:
        cursor.execute('''
            UPDATE platos
            SET nombre = COALESCE(%s, nombre), 
                descripcion = COALESCE(%s, descripcion), 
                precio = COALESCE(%s, precio)
            WHERE id = %s
        ''', (nuevo_nombre, nueva_descripcion, nuevo_precio, plato_id))
        conn.commit()

    # Actualizar los ingredientes
        ingredientes_lista = []
        for ingrediente in nuevos_ingredientes.split(';'):
            # Suponiendo que cada ingrediente tiene el formato "nombre,cantidad"
            nombre, cantidad = ingrediente.split(',')
            ingredientes_lista.append((nombre.strip(), cantidad.strip()))  # Agrega tupla a la lista

        # Actualiza el plato en la base de datos
        cursor.execute(
            "UPDATE platos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s",
            (nuevo_nombre, nueva_descripcion, nuevo_precio, plato_id)
        )

        # Elimina los ingredientes existentes del plato
        cursor.execute("DELETE FROM Plato_Ingredientes WHERE plato_id = %s", (plato_id,))

        # Agrega los nuevos ingredientes al plato
        for nombre_ingrediente, cantidad in ingredientes_lista:
            # Primero, verifica que el ingrediente exista en la base de datos
            cursor.execute("SELECT id FROM ingredientes WHERE nombre = %s", (nombre_ingrediente,))
            resultado = cursor.fetchone()
            if resultado:
                ingrediente_id = resultado[0]
                cursor.execute(
                    "INSERT INTO Plato_Ingredientes (plato_id, ingrediente_id, cantidad) VALUES (%s, %s, %s)",
                    (plato_id, ingrediente_id, cantidad)
                )
            else:
                print(f"Ingrediente '{nombre_ingrediente}' no encontrado. No se puede agregar.")

        # Confirma los cambios en la base de datos
        conn.commit()

    return "Plato modificado exitosamente."
