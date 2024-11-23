import pymysql
import Ingredientes

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
    # Consulta para obtener los platos junto con sus ingredientes y cantidades
    query = """
        SELECT p.id, p.nombre, p.descripcion, p.precio, 
               GROUP_CONCAT(CONCAT(i.nombre, ' ,', pi.cantidad, '') SEPARATOR '; ') AS ingredientes
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
    #Obtiene los datos de la tabla platos
    cursor.execute("SELECT id, nombre, descripcion, precio, imagen FROM platos") 
    Lista_menu = cursor.fetchall()
    return Lista_menu

#Funcion para agregar un plato (Administrador)
def agregar_plato(nombre, descripcion, precio, ingredientes_str, imagen):
    # Inserta el nuevo plato en la tabla platos
    cursor.execute("INSERT INTO platos (nombre, descripcion, precio, imagen) VALUES (%s, %s, %s, %s)", (nombre, descripcion, precio, imagen))
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

#Funcion para Eliminar un plato (Administrador)
def eliminar_plato(plato_id):
    # Se elimina los ingredientes asociados al plato
    cursor.execute("DELETE FROM Plato_Ingredientes WHERE plato_id = %s", (plato_id,))
    
    # Se eliminamos el plato
    cursor.execute("DELETE FROM platos WHERE id = %s", (plato_id,))
    conn.commit()
    
    return "Plato eliminado correctamente." if cursor.rowcount > 0 else "El plato no existe."

#Funcion para modificar un plato (Administrador)
def modificar_plato(plato_id, nuevo_nombre, nueva_descripcion, nuevo_precio, nuevos_ingredientes, imagen):
    # Armar la consulta SQL dinámicamente
    query = '''
        UPDATE platos
        SET nombre = COALESCE(%s, nombre),
            descripcion = COALESCE(%s, descripcion),
            precio = COALESCE(%s, precio)
    '''
    params = [nuevo_nombre, nueva_descripcion, nuevo_precio]

    # Agregar imagen solo si no es None
    if imagen is not None:
        query += ", imagen = %s"
        params.append(imagen)

    query += " WHERE id = %s"
    params.append(plato_id)

    # Ejecutar la consulta SQL
    cursor.execute(query, params)
    conn.commit()

    # Actualizar los ingredientes
    ingredientes_lista = []
    for ingrediente in nuevos_ingredientes.split(';'):
        nombre, cantidad = ingrediente.split(',')
        ingredientes_lista.append((nombre.strip(), cantidad.strip()))

    # Eliminar los ingredientes existentes del plato
    cursor.execute("DELETE FROM Plato_Ingredientes WHERE plato_id = %s", (plato_id,))

    # Agregar los nuevos ingredientes al plato
    for nombre_ingrediente, cantidad in ingredientes_lista:
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

# Función para verificar si un plato está disponible según la cantidad de sus ingredientes

def plato_disponible(plato_id, cantidad_plato):
    try:
        cursor.execute("""
            SELECT i.id, pp.cantidad
            FROM Plato_Ingredientes pp
            JOIN ingredientes i ON pp.ingrediente_id = i.id
            WHERE pp.plato_id = %s
        """, (plato_id,))
        
        ingredientes = cursor.fetchall()
        
        # Flag para verificar si algún ingrediente no tiene suficiente stock
        plato_disponible = True
        
        for ingrediente_id, cantidad_ingrediente in ingredientes:
            cantidad_requerida = cantidad_ingrediente * cantidad_plato
            
            cursor.execute("SELECT stock FROM ingredientes WHERE id = %s", (ingrediente_id,))
            stock_disponible = cursor.fetchone()
            
            if stock_disponible is None or stock_disponible[0] < cantidad_requerida:
                print(f"Ingrediente ID: {ingrediente_id}, Cantidad por Plato: {cantidad_ingrediente}, Cantidad Requerida: {cantidad_requerida}, Stock Disponible: {stock_disponible}")
                plato_disponible = False  # Si hay un ingrediente con falta de stock, marca el plato como no disponible
        
        return plato_disponible  # Retorna True si todos los ingredientes tienen suficiente stock, False si no
    
    except pymysql.MySQLError as e:
        print(f"Error en la base de datos: {e}")
        return False






    
def restar_ingrediente(plato_id, cantidad):
    try:
         # Obtener los ingredientes necesarios para ese plato
        cursor.execute("SELECT ingrediente_id, cantidad FROM Plato_Ingredientes WHERE plato_id = %s", (plato_id,))
        ingredientes = cursor.fetchall()

        # Restar la cantidad de cada ingrediente utilizado
        for ingrediente in ingredientes:
            ingrediente_id, cantidad_ingrediente = ingrediente
            nueva_cantidad = cantidad_ingrediente * cantidad  # La cantidad necesaria depende de la cantidad de platos
            cursor.execute("""
                UPDATE ingredientes
                SET stock = stock - %s
                WHERE id = %s
            """, (nueva_cantidad, ingrediente_id))
        
        conn.commit()
        print(f"Ingredientes restados para el plato {plato_id}.")
    except pymysql.MySQLError as e:
        return f"Error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"


def obtener_cantidad_disponible(ingrediente_id):
    try:
        # Obtiene la cantidad disponible del ingrediente
        query = "SELECT stock FROM ingredientes WHERE id = %s"
        cursor.execute(query, (ingrediente_id,))
        cantidad = cursor.fetchone()

        if cantidad:
            return cantidad[0]  # Retorna la cantidad disponible del ingrediente
        else:
            return f"No se encontró el ingrediente con ID {ingrediente_id}."
    except pymysql.MySQLError as e:
        return f"Error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"
