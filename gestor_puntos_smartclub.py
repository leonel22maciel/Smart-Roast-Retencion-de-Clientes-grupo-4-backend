class Cliente:
    def __init__(self, nombre, plan):
        self.nombre = nombre
        self.plan = plan
        self.puntos = 0
        self.compras = []
        self.canjes = []

    def es_premium(self):
        return self.plan.nombre.lower() == "premium"

    def sumar_puntos(self, puntos):
        self.puntos += puntos

    def descontar_puntos(self, puntos):
        if self.puntos < puntos:
            return False

        self.puntos -= puntos
        return True


class Plan:
    def __init__(self, nombre, precio, multiplica_puntos):
        self.nombre = nombre
        self.precio = precio
        self.multiplica_puntos = multiplica_puntos

class Compra:
    def __init__(self, producto, monto, puntos):
        self.producto = producto
        self.monto = monto
        self.puntos = puntos

    def resumen(self):
        return f"{self.producto} - ${self.monto} - {self.puntos} puntos"

class Recompensa:
    def __init__(self, nombre, costo, solo_premium=False):
        self.nombre = nombre
        self.costo = costo
        self.solo_premium = solo_premium

    def puede_canjearla(self, cliente):
        if self.solo_premium and not cliente.es_premium():
            return False

        return True

