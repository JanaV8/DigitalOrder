
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