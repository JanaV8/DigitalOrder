import pymysql

#Conexion con la Base de Datos
conn = pymysql.connect( 
        host='26.92.40.13',
        user='root',
        password='',
        database='administrador_bd')
cursor = conn.cursor()

#Crea una tabla para Administradores en caso de que no exista
cursor.execute('''
CREATE TABLE IF NOT EXISTS administradores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    contraseña INTEGER  
)
''')

#Funcion para Agregar un Administrador
def agregar_administrador(usuario,contraseña):
    try:
        #se insertan los usuarios y contraseña en la tabla Administradores
        cursor.execute('INSERT INTO administradores(usuario, contraseña) VALUES (%s, %s)', (usuario, contraseña)) #se insertan los usuarios y contraseña en la tabla Administradores
        conn.commit()
        
        return 'Se agrego el usuario Correctamente'
    except pymysql.IntegrityError:
        return 'Usuario existente'
    
#Funcion para Eliminar un Administrador     
def eliminar_administrador(id_ingresada):
    try:
    #Elimina un administrador tomando su id como referencia 
        cursor.execute("DELETE FROM administradores WHERE id = %s", (id_ingresada)) 
        conn.commit()

        if cursor.rowcount > 0:
            return "Administrador Eliminado exitosamente."
        else:
            return "El administrador no existe."
    # Cracion de excepciones para los posibles errores    
    except pymysql.IntegrityError:
        return "No se puede eliminar el administrador. El registro está vinculado a otros datos."
    except pymysql.OperationalError as e:
        return f"Error de operación en la base de datos: {e}"
    except pymysql.MySQLError as e:
        return f"Ocurrió un error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

#Funcion para Validar un Administrador
def validar_administrador (usuarioIngresado,contraseñaIngresado):
    try:
        #Valida si los datos ingresados coincden con los que estan en la base de datos
        cursor.execute('SELECT * FROM administradores WHERE usuario=%s AND contraseña=%s', (usuarioIngresado,contraseñaIngresado)) 
        resultado =cursor.fetchone()
    
        if resultado:    
        
            return True
        else:
            return False        
    # Cracion de excepciones para los posibles errores
    except pymysql.OperationalError as e:
        return f"Error de operación en la base de datos: {e}"
    except pymysql.MySQLError as e:
        return f"Ocurrió un error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"
    
#Funcion para Actualizar los Datos del Administrador
def actualizar_administrador (id_ingresado, nombre_nuevo = None, contraseña_nueva = None):
    try:
        #Toma los datos ingresados en los campos y los actualiza en la base de datos tomando como referencia la id 
        if nombre_nuevo != None and contraseña_nueva != None:
            cursor.execute("UPDATE administradores SET usuario = %s, contraseña = %s WHERE id = %s ", (nombre_nuevo, contraseña_nueva, id_ingresado))  
        elif nombre_nuevo:
            cursor.execute("UPDATE administradores SET usuario = %s WHERE id = %s", (nombre_nuevo, id_ingresado))
        elif contraseña_nueva:
            cursor.execute("UPDATE administradores SET contraseña = %s WHERE id = %s", (contraseña_nueva, id_ingresado))
        else:
            return "No hay valores que actualizar."
        conn.commit()
    # Cracion de excepciones para los posibles errores
    except pymysql.IntegrityError:
        return "No se puede actualizar el administrador. El nombre de usuario ya existe."
    except pymysql.OperationalError as e:
        return f"Error de operación en la base de datos: {e}"
    except pymysql.MySQLError as e:
        return f"Ocurrió un error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"    

#Funcion para mostrar Administradores
def obtener_administradores():
    try:
        #Obtiene los datos de los administradores de la base de datos
        cursor.execute("SELECT id, usuario, contraseña FROM administradores")  
        administradores = cursor.fetchall()
        return administradores
    # Cracion de excepciones para los posibles errores
    except pymysql.OperationalError as e:
        return f"Error de operación en la base de datos: {e}"
    except pymysql.MySQLError as e:
        return f"Ocurrió un error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

