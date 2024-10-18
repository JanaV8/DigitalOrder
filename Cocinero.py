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
    cursor.execute("SELECT usuario FROM cocineros")
    cocineros = cursor.fetchall()
    return [cocinero[0] for cocinero in cocineros] 

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
        cursor.execute("DELETE FROM cocineros WHERE id = %s", (id_ingresada))
        conn.commit()

        # Verificar si realmente se eliminó alguna fila y muestra un mensaje dependiendo del caso
        if cursor.rowcount > 0:
            return "Cocineros Eliminado exitosamente."
        else:
            return "El Cocinero no existe."

def validar_Cocinero (usuarioIngresado,contraseñaIngresado):

    cursor.execute('SELECT * FROM cocineros WHERE usuario=%s AND contraseña=%s', (usuarioIngresado,contraseñaIngresado))
    resultado =cursor.fetchone()

    if resultado:
        #Retornamos un mensaje de acceso Concedido
        return True
        #Llamamos la funcion para cambiar el GUI
    else:
        return False
