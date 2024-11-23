import pymysql

#Conexion con la Base de Datos
conn = pymysql.connect( 
        host='26.92.40.13',
        user='root',
        password='',
        database='mozo_bd')
cursor = conn.cursor()

#Crea una tabla para mozos en caso de que no exista
cursor.execute('''
CREATE TABLE IF NOT EXISTS mozos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    contraseña INTEGER  
)
''')

#Funcion para Agregar un mozo
def agregar_mozo(usuario,contraseña):
    try:
        #se insertan los usuarios y contraseña en la tabla mozos
        cursor.execute('INSERT INTO mozos(usuario, contraseña) VALUES (%s, %s)', (usuario, contraseña)) #se insertan los usuarios y contraseña en la tabla Administradores
        conn.commit()
        
        return 'Se agrego el usuario Correctamente'
    except pymysql.IntegrityError:
        return 'Usuario existente'
    
#Funcion para Eliminar un mozo     
def eliminar_mozo(id_ingresada):
    #Elimina un administrador tomando su id como referencia 
        cursor.execute("DELETE FROM mozos WHERE id = %s", (id_ingresada)) 
        conn.commit()

        if cursor.rowcount > 0:
            return "Mozo eliminado exitosamente."
        else:
            return "El mozo no existe."

#Funcion para Validar un mozo
def validar_mozo (usuarioIngresado,contraseñaIngresado):
    #Valida si los datos ingresados coincden con los que estan en la base de datos
    cursor.execute('SELECT * FROM mozos WHERE usuario=%s AND contraseña=%s', (usuarioIngresado,contraseñaIngresado)) 
    resultado =cursor.fetchone()
    
    if resultado:    
        
        return True
    else:
        return False           

#Funcion para Actualizar los Datos del mozo
def actualizar_mozo (id_ingresado, nombre_nuevo = None, contraseña_nueva = None):
    #Toma los datos ingresados en los campos y los actualiza en la base de datos tomando como referencia la id 
    if nombre_nuevo != None and contraseña_nueva != None:
        cursor.execute("UPDATE mozos SET usuario = %s, contraseña = %s WHERE id = %s ", (nombre_nuevo, contraseña_nueva, id_ingresado))  
    elif nombre_nuevo:
        cursor.execute("UPDATE mozos SET usuario = %s WHERE id = %s", (nombre_nuevo, id_ingresado))
    elif contraseña_nueva:
        cursor.execute("UPDATE mozos SET contraseña = %s WHERE id = %s", (contraseña_nueva, id_ingresado))
    else:
        return "No hay valores que actualizar."
    conn.commit()

#Funcion para mostrar mozos
def obtener_mozos():
    #Obtiene los datos de los mozos de la base de datos
    cursor.execute("SELECT id, usuario, contraseña FROM mozos")  
    mozos = cursor.fetchall()
    return mozos