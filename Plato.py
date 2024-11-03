import pymysql

conn = pymysql.connect( 
        host='26.92.40.13',
        user='root',
        password='',
        database='platos_bd')
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

# Crear la tabla Plato_Ingredientes
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

#Funcion para mostrar los platos al administrador
def mostrar_platos():
    try:
        # Consulta para obtener los platos junto con sus ingredientes y cantidades
        query = """
            SELECT p.id, p.nombre, p.descripcion, p.precio, 
                GROUP_CONCAT(CONCAT(i.nombre, ' ,', pi.cantidad, '') SEPARATOR ', ') AS ingredientes
            FROM platos p
            LEFT JOIN Plato_Ingredientes pi ON p.id = pi.plato_id
            LEFT JOIN ingredientes i ON pi.ingrediente_id = i.id
            GROUP BY p.id
        """
        cursor.execute(query)
        Lista_platos = cursor.fetchall()
        return Lista_platos
    
    # Cracion de excepciones para los posibles errores
    except pymysql.MySQLError as e:
        return f"Error al mostrar platos: {e}"

#Funcion para mostrar el menu al cliente
def mostrar_menu ():
    try:
        #Obtiene los datos de la tabla platos
        cursor.execute("SELECT nombre, descripcion, precio FROM platos") 
        Lista_menu = cursor.fetchall()
        return Lista_menu
    # Cracion de excepciones para los posibles errores
    except pymysql.MySQLError as e:
        return f"Error al mostrar menú: {e}"

#Funcion para agregar un plato (Administrador)
def agregar_plato(nombre, descripcion, precio, ingredientes_str):
    try:    
        # Inserta el nuevo plato en la tabla platos
        cursor.execute("INSERT INTO platos (nombre, descripcion, precio) VALUES (%s, %s, %s)", (nombre, descripcion, precio))
        # Obtiene el ID del plato recién agregado
        plato_id = cursor.lastrowid 

        # Separa el string de ingredientes en partes
        ingredientes = ingredientes_str.split(';') if ingredientes_str else []

        for ingrediente in ingredientes:
            # Separa el nombre y cantidad
            if ',' in ingrediente:
                # Limita a 1 la separación
                nombre_ingrediente, cantidad = ingrediente.split(',', 1) 
                # Elimina los espacios 
                nombre_ingrediente = nombre_ingrediente.strip()  
                cantidad = cantidad.strip()

                # Busca el ID del ingrediente basado en su nombre
                cursor.execute("SELECT id FROM ingredientes WHERE nombre = %s", (nombre_ingrediente,))
                resultado = cursor.fetchone()

                # Si se encontró el ingrediente
                if resultado:  
                    #Obtiene el ID
                    ingrediente_id = resultado[0] 
                    # Inserta la ID del plato e ingrediente y la cantidad del ingrediente en la tabla Plato_Ingrediente
                    cursor.execute("INSERT INTO Plato_Ingredientes (plato_id, ingrediente_id, cantidad) VALUES (%s, %s, %s)", (plato_id, ingrediente_id, cantidad))
                else:
                    return f"Ingrediente '{nombre_ingrediente}' no existe. El plato no fue agregado."
            else:
                return "Formato incorrecto para el ingrediente. Debe ser 'nombre,cantidad'."
        # Confirmar cambios
        conn.commit()
        return "Plato agregado exitosamente."
    # Cracion de excepciones para los posibles errores
    except pymysql.IntegrityError:
        return "Error de integridad al agregar el plato. Verifique datos únicos o relaciones."
    except pymysql.MySQLError as e:
        return f"Error al agregar plato: {e}"

#Funcion para Eliminar un plato (Administrador)
def eliminar_plato(plato_id):
    try:    
        # Se elimina los ingredientes asociados al plato
        cursor.execute("DELETE FROM Plato_Ingredientes WHERE plato_id = %s", (plato_id,))
    
        # Se eliminamos el plato
        cursor.execute("DELETE FROM platos WHERE id = %s", (plato_id,))
        conn.commit()
    
        return "Plato eliminado correctamente." if cursor.rowcount > 0 else "El plato no existe."
     # Cracion de excepciones para los posibles errores
    except pymysql.MySQLError as e:
        return f"Error al eliminar el plato: {e}"
    


#Funcion para modificar un plato (Administrador)
def modificar_plato(plato_id, nuevo_nombre, nueva_descripcion, nuevo_precio, nuevos_ingredientes):
    try:
        # Actualiza los datos del plato
        if nuevo_nombre is not None or nueva_descripcion is not None or nuevo_precio is not None:
            cursor.execute('''
                UPDATE platos
                SET nombre = COALESCE(%s, nombre), 
                    descripcion = COALESCE(%s, descripcion), 
                    precio = COALESCE(%s, precio)
                WHERE id = %s
            ''', (nuevo_nombre, nueva_descripcion, nuevo_precio, plato_id))
            conn.commit()

            # Actualiza los ingredientes
            ingredientes_lista = []
            for ingrediente in nuevos_ingredientes.split(';'):
                nombre, cantidad = ingrediente.split(',')
                # Agrega tupla a la lista
                ingredientes_lista.append((nombre.strip(), cantidad.strip()))  

            # Actualiza el plato en la base de datos
            cursor.execute(
                "UPDATE platos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s",
                (nuevo_nombre, nueva_descripcion, nuevo_precio, plato_id)
            )

            # Elimina los ingredientes existentes del plato
            cursor.execute("DELETE FROM Plato_Ingredientes WHERE plato_id = %s", (plato_id,))

            # Agrega los nuevos ingredientes al plato
            for nombre_ingrediente, cantidad in ingredientes_lista:
                # Verifica que el ingrediente exista en la base de datos
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
            conn.commit()
        return "Plato modificado exitosamente."
    # Cracion de excepciones para los posibles errores
    except pymysql.IntegrityError:
        return "Error de integridad al modificar el plato. Verifique datos únicos o relaciones."
    except pymysql.MySQLError as e:
        return f"Error al modificar plato: {e}"