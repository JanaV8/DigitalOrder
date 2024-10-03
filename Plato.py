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

def mostrar_platos ():
    cursor.execute("SELECT id, nombre, descripcion, precio FROM platos")
    Lista_platos = cursor.fetchall()
    return Lista_platos

#Funcion para mostrar el menu al cliente
def mostrar_menu ():
    cursor.execute("SELECT nombre, descripcion, precio FROM platos")
    Lista_menu = cursor.fetchall()
    return Lista_menu

def agregar_plato(nombre, descripcion, precio, ingredientes):

    # Insertar el nuevo plato
    cursor.execute("INSERT INTO platos (nombre, descripcion, precio) VALUES (%s, %s, %s)", (nombre, descripcion, precio))
    plato_id = cursor.lastrowid  # Obtener el ID del plato recién agregado

    for nombre_ingrediente, cantidad in ingredientes:
        # Buscar el ID del ingrediente basado en su nombre
        cursor.execute("SELECT id FROM ingredientes WHERE nombre = %s", (nombre_ingrediente,))
        resultado = cursor.fetchone()

        if resultado:  # Si se encontró el ingrediente
            ingrediente_id = resultado[0]  # Obtener el ID
            cursor.execute("INSERT INTO Plato_Ingredientes (plato_id, ingrediente_id, cantidad) VALUES (%s, %s, %s)", (plato_id, ingrediente_id, cantidad))
        else:
            return f"Ingrediente '{nombre_ingrediente}' no existe. El plato no fue agregado."

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

def modificar_plato(plato_id, nuevo_nombre=None, nueva_descripcion=None, nuevo_precio=None, nuevos_ingredientes=None):
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
    if nuevos_ingredientes is not None:
        # Primero eliminamos los ingredientes existentes
        cursor.execute('DELETE FROM Plato_Ingredientes WHERE plato_id = %s', (plato_id,))
        
        # Luego insertamos los nuevos ingredientes solo si se proporcionan
        if nuevos_ingredientes:  # Verifica si hay nuevos ingredientes
            for nombre_ingrediente, cantidad in nuevos_ingredientes:
                # Busca el ID del ingrediente
                cursor.execute("SELECT id FROM ingredientes WHERE nombre = %s", (nombre_ingrediente,))
                resultado = cursor.fetchone()

                if resultado:  # Si se encontró el ingrediente
                    ingrediente_id = resultado[0]
                    cursor.execute('INSERT INTO Plato_Ingredientes (plato_id, ingrediente_id, cantidad) VALUES (%s, %s, %s)', (plato_id, ingrediente_id, cantidad))
                else:
                    return f"Ingrediente '{nombre_ingrediente}' no existe. No se ha agregado al plato."

        conn.commit()

    return "Plato modificado exitosamente."
