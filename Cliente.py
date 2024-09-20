from Pedido import Pedido

#Clase cliente con sus variables
class Cliente:
    def __init__(self, numero_mesa):
        self.numero_mesa = numero_mesa
        self.pedido = Pedido()  # Pedido que el cliente va a realizar
    
    #Funcion para selecionar la mesa
    def seleccionarMesa(self) -> int:
        return self.numero_mesa
    
    #Funcion para seleccionar el Plato 
    def seleccionarPlato(self, plato):
        self.pedido.agregar_plato(plato)
    
    #Funcion para confirmar el Pedido
    def aceptarPedido(self):
        self.pedido.estado = 'Aceptado'
        print(f"Pedido de la mesa {self.numero_mesa} aceptado.")
    
    #Funcion para cancelar un Pedido
    def cancelarPedido(self):
        self.pedido.platos.clear()
        self.pedido.estado = 'Cancelado'
        print(f"Pedido de la mesa {self.numero_mesa} cancelado.")
    
    #Funcion para modificar un Pedido
    def modificarPedido(self, plato_a_eliminar, plato_a_agregar):
        self.pedido.eliminar_plato(plato_a_eliminar)
        self.pedido.agregar_plato(plato_a_agregar)
        print(f"Pedido modificado para la mesa {self.numero_mesa}.")