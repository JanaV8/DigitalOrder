import pymysql

conn = pymysql.connect( 
        host='26.92.40.13',
        user='root',
        password='',
        database='plato_bd')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS platos (
    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL
)
''')
#Clase plato con sus variables
class Plato:
    def __init__(self, nombre, precio, descripcion):
        self.nombre = nombre
        self.precio = precio
        self.ingredientes = []
        self.descripcion = descripcion
        self.estado = 'Pendiente'
    
    #Funcion para mostrar el menu
    def mostrarPlatos(self) -> list:
        return [self.nombre, self.precio, self.ingredientes, self.descripcion]
    
    #Funcion para cambiar el estado de un plato (Pendiente y Listo)
    def cambiar_estado(self):
        if self.estado == 'Pendiente':
            self.estado = 'Listo'
        else:
            self.estado = 'Pendiente'
    
    #Funcion que muestra el estado del pedido
    def __str__(self):
        return f"Plato: {self.nombre}, Estado: {self.estado}"

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

def agregar_plato(nombre , descripcion, precio, ingredientes):
    try:
        cursor.execute("INSERT INTO platos (nombre, descripcion, precio) VALUES (%s,%s,%s)", (nombre, descripcion, precio))
        plato_id =cursor.lastrowid
    
        # Insertar ingredientes en la tabla de relación
        for ingrediente_id, cantidad in ingredientes:
            # Verificar si el ingrediente existe en la base de datos
            cursor.execute("SELECT id FROM ingredientes WHERE id = %s", (ingrediente_id,))
            if cursor.fetchone() is not None:  # Solo agregar si el ingrediente existe
                cursor.execute("INSERT INTO Plato_Ingredientes (plato_id, ingrediente_id, cantidad) VALUES (%s, %s, %s)", (plato_id, ingrediente_id, cantidad))
            else:
                return f"Ingrediente con ID {ingrediente_id} no existe. El plato no fue agregado."
        
        conn.commit()
        return "Plato agregado exitosamente."
    except Exception as e:
        return f"Ocurrió un error al agregar el plato: {e}"


conn.close()