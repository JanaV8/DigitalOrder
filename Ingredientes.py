import pymysql

conn = pymysql.connect( 
        host='26.92.40.13',
        user='root',
        password='',
        database='plato_bd')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ingredientes (
    
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    stock REAL NOT NULL
)
''')
    
#Funcion para añadir un ingrediente
def añadir_ingrediente(nombre_ingresado, cantidad_ingresada):
    try:
        
        cursor.execute('INSERT INTO ingredientes(nombre, stock) VALUES (%s, %s)', (nombre_ingresado, cantidad_ingresada))
        conn.commit()
        
        #Retornamos un mensaje de exito o de ya existencia dependiendo del caso
        return 'Se agrego el ingrediente correctamente'
    except pymysql.IntegrityError:
        return 'ingrediente existente existente'
    finally:
        # ver si funciona seguramente tendriamosque sacarlo de aca
        conn.close()
#Necesitariamos una funcion en donde mostraria la base de datos al administrador 
def mostrar_BD_Ingredientes (id_seleccionado):
    cursor.execute("SELECT id, nombre, stock FROM ingredientes WHEREE id = %s", (id_seleccionado))
    resultado = cursor.fetchall()
    
#Funcion para modificar un ingrediente
def modificar_ingrediente(id_seleccionado, nombre_nuevo = None ,cantidad_nueva = None ):
    
    if nombre_nuevo != None and cantidad_nueva != None:
        cursor.execute("UPDATE ingredientes SET nombre = %s, stock = %s WHERE id = %s ", (nombre_nuevo, cantidad_nueva, id_seleccionado))  
    elif nombre_nuevo:
        cursor.execute("UPDATE ingredientes SET nombre = %s WHERE id = %s", (nombre_nuevo, id_seleccionado))
    elif cantidad_nueva:
        cursor.execute("UPDATE ingredientes SET stock = %s WHERE id = %s", (cantidad_nueva, id_seleccionado))
    else:
        return "No hay valores que actualizar."
    conn.commit()

def eliminar_ingrediente(id_seleccionado):
    try:
        # Eliminar el ingrediente
        cursor.execute("DELETE FROM ingredientes WHERE id = %s", (id_seleccionado))
        conn.commit()

        # Verificar si realmente se eliminó alguna fila
        if cursor.rowcount > 0:
            return "Ingrediente eliminado exitosamente."
        else:
            return "El Ingrediente no existe."
    finally:
        conn.close()
