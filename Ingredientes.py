import pymysql

#Conexion con la Base de Datos
conn = pymysql.connect( 
        host='26.92.40.13',
        user='root',
        password='',
        database='platos_bd')
cursor = conn.cursor()


#Crea una tabla para Ingredientes en caso de que no exista
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
        #Agrega ingredientes a la tabla tomando su nombre y cantidad
        cursor.execute('INSERT INTO ingredientes(nombre, stock) VALUES (%s, %s)', (nombre_ingresado, cantidad_ingresada))
        conn.commit()
        
        return 'Se agrego el ingrediente correctamente'
    except pymysql.IntegrityError:
        return 'ingrediente inexistente'

#Funcion para mostrar Ingredientes
def mostrar_bd_Ingredientes ():
    #Obtiene los datos de los ingredientes de la base de datos
    cursor.execute("SELECT id, nombre, stock FROM ingredientes")
    Lista_ingredientes = cursor.fetchall()
    return Lista_ingredientes
    
#Funcion para modificar un ingrediente
def modificar_ingrediente(id_seleccionado, nombre_nuevo = None ,cantidad_nueva = None ):
    
     #Toma los datos ingresados en los campos y los actualiza en la base de datos tomando como referencia la ID 
    if nombre_nuevo != None and cantidad_nueva != None:
        cursor.execute("UPDATE ingredientes SET nombre = %s, stock = %s WHERE id = %s ", (nombre_nuevo, cantidad_nueva, id_seleccionado))  
    elif nombre_nuevo:
        cursor.execute("UPDATE ingredientes SET nombre = %s WHERE id = %s", (nombre_nuevo, id_seleccionado))
    elif cantidad_nueva:
        cursor.execute("UPDATE ingredientes SET stock = %s WHERE id = %s", (cantidad_nueva, id_seleccionado))
    else:
        return "No hay valores que actualizar."
    conn.commit()

#Funcion para eliminar un ingrediente
def eliminar_ingrediente(id_seleccionado):  
    # Eliminar el ingrediente tomando la ID como referencia
    cursor.execute("DELETE FROM ingredientes WHERE id = %s", (id_seleccionado))
    conn.commit()

    if cursor.rowcount > 0:
        return "Ingrediente eliminado exitosamente."
    else:
        return "El Ingrediente no existe."
    