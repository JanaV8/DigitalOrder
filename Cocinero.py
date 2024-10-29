import pymysql


#Conexion con la Base de Datos
conn = pymysql.connect( 
        host='26.92.40.13',
        user='root',
        password='',
        database='cocineros_bd')
cursor = conn.cursor()

#Crea una Tabla en Caso de que no Exista
cursor.execute('''
CREATE TABLE IF NOT EXISTS cocineros (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    contraseña INTEGER
)
''')


def obtener_cocineros():
    try:
        cursor.execute("SELECT usuario FROM cocineros")
        cocineros = cursor.fetchall()
        return [cocinero[0] for cocinero in cocineros]
    # Cracion de excepciones para los posibles errores
    except pymysql.OperationalError as e:
        return f"Error de operación en la base de datos: {e}"
    except pymysql.MySQLError as e:
        return f"Ocurrió un error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}" 

#Clase cocinero con las variables nombre y contraseña
def agregar_Cocineros(usuario,contraseña):
    try:
        cursor.execute('INSERT INTO cocineros(usuario, contraseña) VALUES (%s, %s)', (usuario, contraseña))
        conn.commit()

        #Retornamos un mensaje de exito o de ya existencia dependiendo del caso
        return True
    except pymysql.IntegrityError:
        return False
 
def eliminar_Cocineros(id_ingresada):
    try:
        cursor.execute("DELETE FROM cocineros WHERE id = %s", (id_ingresada))
        conn.commit()

        # Verificar si realmente se eliminó alguna fila y muestra un mensaje dependiendo del caso
        if cursor.rowcount > 0:
            return "Cocineros Eliminado exitosamente."
        else:
            return "El Cocinero no existe."
    # Cracion de excepciones para los posibles errores    
    except pymysql.IntegrityError:
        return "No se puede eliminar el cocinero. El registro está vinculado a otros datos."
    except pymysql.OperationalError as e:
        return f"Error de operación en la base de datos: {e}"
    except pymysql.MySQLError as e:
        return f"Ocurrió un error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"
        

def validar_Cocinero (usuarioIngresado,contraseñaIngresado):    
    try:
        cursor.execute('SELECT * FROM cocineros WHERE usuario=%s AND contraseña=%s', (usuarioIngresado,contraseñaIngresado))
        resultado =cursor.fetchone()

        if resultado:
            #Retornamos un mensaje de acceso Concedido
            return True
            #Llamamos la funcion para cambiar el GUI
        else:
            return False
    # Cracion de excepciones para los posibles errores    
    except pymysql.OperationalError as e:
        return f"Error de operación en la base de datos: {e}"
    except pymysql.MySQLError as e:
        return f"Ocurrió un error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"
        
#Funcion para mostrar Cocineros
def obt_cocineros():
    try:
        #Obtiene los datos de los cocineros de la base de datos
        cursor.execute("SELECT id, usuario, contraseña FROM cocineros")  
        cocineros = cursor.fetchall()
        return cocineros
    # Cracion de excepciones para los posibles errores
    except pymysql.OperationalError as e:
        return f"Error de operación en la base de datos: {e}"
    except pymysql.MySQLError as e:
        return f"Ocurrió un error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

#Funcion para Actualizar los Datos del Cocinero
def modificar_cocinero (id_ingresado, nombre_nuevo = None, contraseña_nueva = None):
    try:
        #Toma los datos ingresados en los campos y los actualiza en la base de datos tomando como referencia la id 
        if nombre_nuevo != None and contraseña_nueva != None:
            cursor.execute("UPDATE cocineros SET usuario = %s, contraseña = %s WHERE id = %s ", (nombre_nuevo, contraseña_nueva, id_ingresado))  
        elif nombre_nuevo:
            cursor.execute("UPDATE cocineros SET usuario = %s WHERE id = %s", (nombre_nuevo, id_ingresado))
        elif contraseña_nueva:
            cursor.execute("UPDATE cocineros SET contraseña = %s WHERE id = %s", (contraseña_nueva, id_ingresado))
        else:
            return "No hay valores que actualizar."
        conn.commit()
    # Cracion de excepciones para los posibles errores     
    except pymysql.IntegrityError:
        return "No se puede actualizar el cocinero. El nombre de usuario ya existe."
    except pymysql.OperationalError as e:
        return f"Error de operación en la base de datos: {e}"
    except pymysql.MySQLError as e:
        return f"Ocurrió un error en la base de datos: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"  