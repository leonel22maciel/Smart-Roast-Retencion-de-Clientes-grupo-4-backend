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