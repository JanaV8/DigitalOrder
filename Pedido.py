
#Clase pedido con sus variables
class Pedido:
    def __init__(self, numero_mesa):
        self.numero_mesa = numero_mesa
        self.platos = []
        self.estado = "Pendiente"
        self.precio_final = 0.0
    
    #Funcion para agregar un plato
    def agregar_plato(self, plato):
        self.platos.append(plato)
        print(f"Plato {plato.nombre} agregado al pedido.")
    
    #Funcion para eliminar un plato
    def eliminar_plato(self, plato):
        if plato in self.platos:
            self.platos.remove(plato)
            print(f"Plato {plato.nombre} eliminado del pedido.")
        else:
            print(f"El plato {plato.nombre} no está en el pedido.")

    #Funcion para mostrar el estado del plato
    def __str__(self):
        platos_str = ', '.join([plato.nombre for plato in self.platos])
        return f"Pedido: {platos_str}, Estado: {self.estado}"
    
    #Funcion para calcular el precio final del pedido
    def calcularPrecio(self) -> float:
        self.precio_final = sum(plato.precio for plato in self.platos)
        return self.precio_final