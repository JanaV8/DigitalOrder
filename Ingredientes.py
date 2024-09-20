class Ingredientes:
    def __init__(self, id, nombre, cantidad_unidad, cantidad_peso):
        self.id = id
        self.nombre = nombre
        self.cantidad_unidad = cantidad_unidad
        self.cantidad_peso = cantidad_peso
    
    def mostrarIngredientes(self) -> list:
        return [self.id, self.nombre, self.cantidad_unidad, self.cantidad_peso]