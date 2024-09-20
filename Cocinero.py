import Plato

#Clase cocinero con las variables nombre y contraseña
class Cocinero:
    def __init__(self, nombre, contraseña):
        self.nombre = nombre
        self.contrasena = contraseña
    
    #Funcion para modificar el estado de un Plato el cual hereda de la clase plato
    def modificarEstado(self, plato: Plato) -> bool:
        if plato.estado == 'Pendiente':
            plato.cambiar_estado()
            return True
        else:
            print(f"El plato {plato.nombre} ya está listo.")
            return False
    
    # Implementación pendiente
    #def redireccionarPedido(self):
       # pass