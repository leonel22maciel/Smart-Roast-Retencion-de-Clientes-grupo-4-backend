# =====================================================================
# ESTRUCTURAS DE DATOS INICIALES (Base de datos simulada)
# =====================================================================

configuracion_puntos = {
    "pesos_necesarios": 1000,
    "puntos_ganados": 10
}

cliente_inicial = {
    "nombre": "Lucia",
    "suscripcion": "Premium",
    "saldo_puntos": 0
}

compras_mensuales_inicial = [
    {"producto": "Cafe Colombia 500g", "monto": 18000},
    {"producto": "Cafe Brasil 1kg", "monto": 30000},
    {"producto": "Cafe Molido 250g", "monto": 12000}
]

recompensas_inicial = {
    "1": {"nombre": "Descuento 10%", "costo": 100, "solo_premium": False},
    "2": {"nombre": "Envio gratis", "costo": 150, "solo_premium": False},
    "3": {"nombre": "Taza exclusiva", "costo": 300, "solo_premium": True},
    "4": {"nombre": "Cafe premium gratis", "costo": 500, "solo_premium": True}
}

planes_iniciales = {
    "Basico": {"precio": 0, "beneficio": "Puntos normales", "multiplicador": 1},
    "Explorer": {"precio": 17999, "beneficio": "50% mas puntos", "multiplicador": 1.5},
    "Premium": {"precio": 29999, "beneficio": "Puntos dobles y beneficios VIP", "multiplicador": 2}
}

historial_compras_inicial = []

clientes_ranking_inicial = [
    {"nombre": "Sofia", "suscripcion": "Premium", "total_gastado": 85000},
    {"nombre": "Mateo", "suscripcion": "Premium", "total_gastado": 76000},
    {"nombre": "Valentina", "suscripcion": "Premium", "total_gastado": 63000},
    {"nombre": "Martin", "suscripcion": "Basico", "total_gastado": 90000}
]


# =====================================================================
# SECCION DE FUNCIONES DEL MODULO SMARTCLUB
# =====================================================================

#========== #consigna 1: Calcular puntos por una compra #========
def obtener_multiplicador(suscripcion, planes):
    suscripcion = suscripcion.strip().capitalize()

    if suscripcion in planes:
        return planes[suscripcion]["multiplicador"]

    return 1
