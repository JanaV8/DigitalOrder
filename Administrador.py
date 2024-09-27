import pymysql

conn = pymysql.connect( 
        host='26.92.40.13',
        user='root',
        password='',
        database='administrador_bd')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS administradores (
    usuario TEXT NOT NULL UNIQUE,
    contraseña INTEGER PRIMARY KEY 
)
''')

#Clase Administrador con sus variables
class Administrador:
    def __init__(self, usuario, contraseña):
        self.usuario = usuario
        self.contraseña = contraseña

    #Agregamos a un administrador a la base de datos, se necesita un usuario y una contrasena.
def agregarAdministrador(usuario,contraseña):
    try:
        
        cursor.execute('INSERT INTO administradores(usuario, contraseña) VALUES (%s, %s)', (usuario, contraseña))
        conn.commit()
        
        #Retornamos un mensaje de exito o de ya existencia dependiendo del caso
        return 'Usuario Agregado Correctamente'
    except pymysql.IntegrityError:
        return 'Usuario existente'
    
#Eliminamos un administrador de la base de dato     
def eliminarAdministrador(usuario):
    try:
        # Eliminar el administrador
        cursor.execute("DELETE FROM administradores WHERE usuario = %s", (usuario))
        conn.commit()

        # Verificar si realmente se eliminó alguna fila
        if cursor.rowcount > 0:
            return "Administrador eliminado exitosamente."
        else:
            return "El administrador no existe."
    finally:
        conn.close()

def validarAdministrador (usuarioIngresado,contraseñaIngresado):
    
    cursor.execute('SELECT * FROM administradores WHERE usuario=%s AND contraseña=%s', (usuarioIngresado,contraseñaIngresado))
    resultado =cursor.fetchone()
    
    if resultado:    
        #Retornamos un mensaje de acceso Concedido
        return True
        #Llamamos la funcion para cambiar el GUI
    else:
        return False           
    
 #Funcion para añadir un plato al menu
def añadir_plato(self, plato):
    pass

#Funcion para modificar un plato
def modificar_plato(self, plato):
    pass

#Funcion para eliminar un plato
def eliminar_plato(self, plato):
    pass

#Funcion para añadir un ingrediente
def añadir_ingrediente(self, ingredientes):
    pass

#Funcion para modificar un ingrediente
def modificar_ingrediente(self, ingredientes):
    pass

#Funcion para eliminar un ingrediente
def eliminar_ingrediente(self, ingredientes):
    pass